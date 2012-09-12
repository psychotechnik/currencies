from django.test import TestCase
from money.models import Template, Transaction


class TransactionTest(TestCase):
    fixtures = ['sample_data.json']

    def setUp(self):
        self.deposits = Template.objects.get(id=1)
        self.usd_eur = Template.objects.get(id=2)
        self.eur_usd = Template.objects.get(id=3)
        self.withdraw = Template.objects.get(id=4)
        Transaction(template=self.deposits, source_amount=100.0).save()

    def test_deposits(self):
        transaction = Transaction(template=self.deposits, source_amount=100.0)
        transaction.save()
        self.assertEqual(transaction.destination.balance, 200.0)

    def test_withdrawal(self):
        transaction = Transaction(template=self.withdraw, source_amount=50.0)
        transaction.save()
        self.assertEqual(transaction.source.balance, 50.0)

    def test_exchange(self):
        #
        # Exchange USD to EUR rate 1.5 amount 10 gain 0
        #
        transaction = Transaction(template=self.usd_eur, rate=1.5,
            source_amount=10)
        transaction.save()
        self.assertEqual(transaction.source.balance, 90.0)
        self.assertEqual(transaction.destination.balance, 15.0)
        self.assertEqual(transaction.rest, 15.0)
        self.assertEqual(transaction.gain, None)
        #
        # Exchange USD to EUR rate 1.5 amount 10 gain 0
        #
        transaction = Transaction(template=self.usd_eur, rate=1.5,
            source_amount=10)
        transaction.save()
        self.assertEqual(transaction.source.balance, 80.0)
        self.assertEqual(transaction.destination.balance, 30.0)
        self.assertEqual(transaction.rest, 15.0)
        self.assertEqual(transaction.gain, None)
        #
        # Exchange EUR to USD rate 0.8 amount 10 gain 2
        #
        transaction = Transaction(template=self.eur_usd, rate=0.8,
            source_amount=10)
        transaction.save()
        self.assertEqual(transaction.source.balance, 20.0)
        self.assertEqual(transaction.destination.balance, 88.0)
        self.assertEqual(transaction.rest, 8.0)
        self.assertEqual(transaction.gain, 1.333333333333333)
        #
        # Exchange EUR to USD rate 0.8 amount 10 gain 2
        #
        transaction = Transaction(template=self.eur_usd, rate=0.8,
            source_amount=20)
        transaction.save()
        self.assertEqual(transaction.source.balance, 00.0)
        self.assertEqual(transaction.destination.balance, 104.0)
        self.assertEqual(transaction.rest, 16.0)
        self.assertEqual(transaction.gain, 2.6666666666666665)
