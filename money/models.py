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
    title = models.CharField(max_length=75)
    currency = models.OneToOneField(Currency)
    balance = models.FloatField(default=0.0)
    #    transaction = models.ForeignKey('money.Transaction', null=True)

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

    def get_transactions_amount(self, transactions=None):
        """Calculate transactions amount"""
        balance = 0.0
        for transaction in transactions or self.transactions():
            if transaction.template.source == self:
                balance -= transaction.amount
            else:
                balance += transaction.amount * transaction.rate
        return balance

#    def set_farthest_transaction(self):
#        """Set farthest transaction from the current balance"""
#        balance = 0.0
#        for transaction in self.transactions(template__destination=self):
#            balance += transaction.destination_amount
#            if self.balance <= balance:
#                self.transaction = transaction
#                break
#        self.save()


class Template(models.Model):
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
    template = models.ForeignKey(Template, related_name='transactions')
    rate = models.FloatField(default=1.0)
    source_amount = models.FloatField()
    destination_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    source_balance = models.FloatField(null=True)
    destination_balance = models.FloatField(null=True)
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
        self.destination_amount = self.source_amount * self.rate
        self.rest = self.destination_amount
        if self.template.source:
            self.source_balance = self.template.source.balance - self.source_amount
        if self.template.destination:
            self.destination_balance = (self.template.destination.balance +
                                        self.source_amount * self.rate)
        self.gain = self.get_gain()
        super(Transaction, self).save(force_insert, force_update, using)

    @property
    def source(self):
        return self.template.source

    @property
    def destination(self):
        return self.template.destination

    @property
    def reverse_template(self):
        try:
            reverse = Template.objects.get(source=self.destination,
                destination=self.source)
        except Template.DoesNotExist:
            return None
        return reverse

    def get_gain(self):
        if not self.source or not self.destination or not self.reverse_template:
            return None
        transactions = Transaction.objects.filter(
            template=self.reverse_template, rest__isnull=False).reverse()
        gain = None
        source_rest = self.source_amount
        if transactions.exists():
            gain = 0.0
            for transaction in transactions:
                if source_rest >= transaction.rest:
                    gain += self.destination_amount * transaction.rest / self.source_amount - transaction.source_amount * transaction.rest / transaction.destination_amount
                    source_rest -= transaction.rest
                    Transaction.objects.filter(pk=transaction.pk).update(
                        rest=None)
                else:
                    gain += self.destination_amount * source_rest / self.source_amount - transaction.source_amount * source_rest / transaction.destination_amount
                    source_rest = transaction.rest - source_rest
                    Transaction.objects.filter(pk=transaction.pk).update(
                        rest=source_rest)
                    break
        Transaction.objects.filter(pk=self.pk).update(gain=gain)
        return gain


@receiver(post_save, sender=Transaction)
def do_transaction(sender, instance, created, **kwargs):
    source = instance.source
    destination = instance.destination
    if source:
        source.balance -= instance.source_amount
        source.save()
    if destination:
        destination.balance += instance.source_amount * instance.rate
        destination.save()


@receiver(pre_delete, sender=Transaction)
def undo_transaction(sender, instance, **kwargs):
    source = instance.template.source
    destination = instance.template.destination
    if source:
        source.balance += instance.amount
        source.save()
    if destination:
        destination.balance -= instance.amount * instance.rate
        destination.save()