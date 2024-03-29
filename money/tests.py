from django.contrib.auth.models import User
from django.test import TestCase
from money.models import Template, Transaction


class TransactionTest(TestCase):
    fixtures = ['sample_data.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.deposits = Template.objects.get(id=1)
        self.usd_eur = Template.objects.get(id=2)
        self.eur_usd = Template.objects.get(id=3)
        self.withdraw = Template.objects.get(id=4)
        Transaction(user=self.user, template=self.deposits,
            source_amount=100.0).save()

    def test_deposits(self):
        transaction = Transaction(user=self.user, template=self.deposits,
            source_amount=100.0)
        transaction.save()
        self.assertEqual(transaction.destination.balance, 200.0)

    def test_withdrawal(self):
        transaction = Transaction(user=self.user, template=self.withdraw,
            source_amount=50.0)
        transaction.save()
        self.assertEqual(transaction.source.balance, 50.0)

    def test_exchange(self):
        #
        # Exchange USD to EUR rate 1.5 amount 10 gain 0
        #
        transaction = Transaction(user=self.user, template=self.usd_eur,
            rate=1.5,
            source_amount=10)
        transaction.save()
        self.assertEqual(transaction.source.balance, 90.0)
        self.assertEqual(transaction.destination.balance, 15.0)
        self.assertEqual(transaction.rest, 15.0)
        self.assertEqual(transaction.gain, None)

        #
        # Exchange USD to EUR rate 1.5 amount 10 gain 0
        #
        transaction = Transaction(user=self.user, template=self.usd_eur,
            rate=1.5, source_amount=10)
        transaction.save()
        self.assertEqual(transaction.source.balance, 80.0)
        self.assertEqual(transaction.destination.balance, 30.0)
        self.assertEqual(transaction.rest, 15.0)
        self.assertEqual(transaction.gain, None)

        #
        # Exchange EUR to USD rate 0.8 amount 10 gain 1.333333333333333
        #
        transaction = Transaction.objects.create(user=self.user,
            template=self.eur_usd, rate=0.8, source_amount=10)
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.source.balance, 20.0)
        self.assertEqual(transaction.destination.balance, 88.0)
        self.assertEqual(transaction.rest, 8.0)
        self.assertEqual(transaction.gain, 1.333333333333333)

        #
        # Exchange EUR to USD rate 0.8 amount 20 gain 2.6666666666666665
        #
        transaction = Transaction.objects.create(user=self.user,
            template=self.eur_usd, rate=0.8, source_amount=20)
        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.source.balance, 0.0)
        self.assertEqual(transaction.destination.balance, 104.0)
        self.assertEqual(transaction.rest, 16.0)
        self.assertEqual(transaction.gain, 2.6666666666666665)

        #
        # Delete last  transaction
        #
        transaction.delete()

        transactions = Transaction.objects.filter(template=self.usd_eur)
        self.assertEqual(transactions[0].rest, 15.0)
        self.assertEqual(transactions[1].rest, 5.0)
