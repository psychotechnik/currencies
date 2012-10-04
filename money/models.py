from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch.dispatcher import receiver

class Currency(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class Wallet(models.Model):
    user = models.ForeignKey(User, related_name='wallets')
    title = models.CharField(max_length=75)
    currency = models.OneToOneField(Currency)
    balance = models.FloatField(default=0.0)

    class Meta:
        pass

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'money:wallet:detail', [self.pk, ]

    @property
    def templates(self):
        """Return relative templates"""
        return self.sources.all() | self.destinations.all()

    @property
    def templates_ids(self):
        """Return ids of relative templates"""
        return self.templates.values_list('pk', flat=True)

    def transactions(self, **kwargs):
        """Return relative transactions"""
        return Transaction.objects.filter(template_id__in=self.templates_ids,
            **kwargs)


class Template(models.Model):
    user = models.ForeignKey(User, related_name='templates')
    title = models.CharField(max_length=75)
    source = models.ForeignKey(Wallet, null=True, related_name='sources')
    destination = models.ForeignKey(Wallet, null=True,
        related_name='destinations')

    class  Meta:
        pass

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'money:template:detail', [self.pk, ]


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name='transactions')
    template = models.ForeignKey(Template, related_name='transactions')
    rate = models.FloatField(default=1.0)
    source_amount = models.FloatField()
    destination_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    rest = models.FloatField(null=True)
    gain = models.FloatField(null=True)

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'

    def __unicode__(self):
        return '%s, rate:%s, source:%s, destination:%s' % (
            self.template.title, self.rate, self.source_amount,
            self.destination_amount)

    @models.permalink
    def get_absolute_url(self):
        return 'money:transaction:detail', [self.pk, ]

    def save(self, force_insert=False, force_update=False, using=None):
        self.destination_amount = self.source_amount * (self.source and self.rate or 1)
        self.rest = self.destination_amount
        super(Transaction, self).save(force_insert, force_update, using)


    @property
    def source(self):
        """Source related to this transaction"""
        return self.template.source

    @property
    def destination(self):
        """Destination related to this transaction"""
        return self.template.destination

    @property
    def reverse_template(self):
        """Get a reverse template of the transaction"""
        try:
            reverse = Template.objects.get(source=self.destination,
                destination=self.source)
        except Template.DoesNotExist:
            return None
        return reverse


class Distribution(models.Model):
    """Model used to maintain the rest of relations deleting transactions"""
    transaction = models.ForeignKey(Transaction, related_name='distributions',
        null=True)
    destination = models.ForeignKey(Transaction)
    rest = models.FloatField()


@receiver(post_save, sender=Transaction)
def do_transaction(sender, instance, created, **kwargs):
    source = instance.source
    destination = instance.destination
    if source:
        source.balance -= instance.source_amount
        source.save()
    if destination:
        destination.balance += instance.source_amount * (source and instance.rate or 1)
        destination.save()

    # Calculate gain of the transaction
    gain = None
    if instance.source and instance.destination and instance.reverse_template:
        transactions = Transaction.objects.filter(
            template=instance.reverse_template, rest__isnull=False).reverse()
        source_rest = instance.source_amount
        if transactions.exists():
            gain = 0.0
            for transaction in transactions:
                if source_rest >= transaction.rest:
                    Distribution.objects.create(
                        transaction=instance,
                        destination=transaction,
                        rest=transaction.rest
                    )
                    gain += (instance.destination_amount *
                             transaction.rest / instance.source_amount
                             - transaction.source_amount *
                               transaction.rest / transaction.destination_amount)
                    source_rest -= transaction.rest
                    Transaction.objects.filter(pk=transaction.pk).update(
                        rest=None)
                else:
                    Distribution.objects.create(
                        transaction=instance,
                        destination=transaction,
                        rest=source_rest
                    )
                    gain += (instance.destination_amount *
                             source_rest / instance.source_amount
                             - transaction.source_amount *
                               source_rest / transaction.destination_amount)
                    source_rest = transaction.rest - source_rest
                    Transaction.objects.filter(pk=transaction.pk).update(
                        rest=source_rest)
                    break
    Transaction.objects.filter(pk=instance.pk).update(gain=gain)


@receiver(pre_delete, sender=Transaction)
def undo_transaction(sender, instance, **kwargs):
    source = instance.source
    destination = instance.destination

    # Restore source balance
    if source:
        source.balance += instance.source_amount
        source.save()

    # Restore destination balance
    if destination:
        destination.balance -= instance.destination_amount
        destination.save()

    # Restore rests
    for distribution in instance.distributions.filter(transaction=instance):
        if distribution.destination.rest:
            Transaction.objects.filter(pk=distribution.destination_id).update(
                rest=distribution.destination.rest + distribution.rest)
        else:
            Transaction.objects.filter(pk=distribution.destination_id).update(
                rest=distribution.rest)
