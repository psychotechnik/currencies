from django.core.urlresolvers import  reverse
from django.contrib import messages
from django.views import generic
from money.forms import CurrencyForm, TransactionForm, WalletForm, TemplateForm
from money.models import Currency, Transaction, Wallet, Template

class MessageFormErrorsMixin(object):
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super(MessageFormErrorsMixin, self).form_invalid(form)


class CurrencyList(generic.ListView):
    model = Currency


class CurrencyDetail(generic.DetailView):
    model = Currency


class CurrencyCreate(MessageFormErrorsMixin, generic.CreateView):
    model = Currency
    form_class = CurrencyForm

    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
            'Please fill form fields with currency name, code and'
            ' set activity flag.'
        )
        return super(CurrencyCreate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Currency successfully created.'
        )
        return reverse('money:currency:list')


class CurrencyUpdate(MessageFormErrorsMixin, generic.UpdateView):
    model = Currency
    form_class = CurrencyForm

    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
            'Please fill form fields with currency name, code and'
            ' set activity flag.'
        )
        return super(CurrencyUpdate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Currency successfully updated.'
        )
        return reverse('money:currency:list')


class CurrencyDelete(generic.DeleteView):
    model = Currency

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Currency successfully deleted.'
        )
        return reverse('money:currency:list')


class TransactionList(generic.ListView):
    model = Transaction


class TransactionDetail(generic.DetailView):
    model = Transaction


class TransactionCreate(MessageFormErrorsMixin, generic.CreateView):
    model = Transaction
    form_class = TransactionForm

    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
            'Choice your transaction template, adjust rate and amount.'
        )
        return super(TransactionCreate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Transaction successfully created.'
        )
        return reverse('money:transaction:list')


class TransactionDelete(generic.DeleteView):
    model = Transaction
    form_class = TransactionForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Transaction successfully deleted.'
        )
        return reverse('money:transaction:list')


class LatestTransactionDelete(TransactionDelete):
    def get_object(self, queryset=None):
        latest = Transaction.objects.latest()
        return latest


class WalletList(generic.ListView):
    model = Wallet


class WalletDetail(generic.DetailView):
    model = Wallet

    def get_context_data(self, **kwargs):
        context = super(WalletDetail, self).get_context_data(**kwargs)
        templates = self.object.templates
        transactions = self.object.transactions()
        context['templates'] = templates
        context['transactions'] = transactions
        return context


class WalletCreate(MessageFormErrorsMixin, generic.CreateView):
    model = Wallet
    form_class = WalletForm

    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
            'Enter wallet title and choice currency.'
        )
        return super(WalletCreate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Wallet successfully created.'
        )
        return reverse('money:wallet:list')


class WalletUpdate(MessageFormErrorsMixin, generic.UpdateView):
    model = Wallet
    form_class = WalletForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Wallet successfully updated.'
        )
        return reverse('money:wallet:list')


class WalletDelete(generic.DeleteView):
    model = Wallet
    form_class = WalletForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Wallet successfully deleted.'
        )
        return reverse('money:wallet:list')


class TemplateList(generic.ListView):
    model = Template


class TemplateDetail(generic.DetailView):
    model = Template


class TemplateCreate(MessageFormErrorsMixin, generic.CreateView):
    model = Template
    form_class = TemplateForm
    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
            'Fill template title, one or both source and destination wallets.'
        )
        return super(TemplateCreate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Template successfully created.'
        )
        return reverse('money:template:list')


class TemplateUpdate(MessageFormErrorsMixin, generic.UpdateView):
    model = Template
    form_class = TemplateForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Template successfully updated.'
        )
        return reverse('money:template:list')


class TemplateDelete(generic.DeleteView):
    model = Template

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Template successfully deleted.'
        )
        return reverse('money:template:list')
