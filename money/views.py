from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import  reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import generic
from money.forms import CurrencyForm, TransactionForm, WalletForm, TemplateForm
from money.models import Currency, Transaction, Wallet, Template

class UserObjectsMixin(object):
    def get_queryset(self):
        qs = super(UserObjectsMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class MessageFormErrorsMixin(object):
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super(MessageFormErrorsMixin, self).form_invalid(form)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args,
            **kwargs)


class CurrencyList(LoginRequiredMixin, generic.ListView):
    model = Currency


class CurrencyDetail(LoginRequiredMixin, generic.DetailView):
    model = Currency


class CurrencyCreate(LoginRequiredMixin, MessageFormErrorsMixin,
    generic.CreateView):
    model = Currency
    form_class = CurrencyForm

    @method_decorator(
        user_passes_test(lambda u: u.has_perm('money.create_currency')))
    def dispatch(self, request, *args, **kwargs):
        return super(CurrencyCreate, self).dispatch(request, *args, **kwargs)

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

    def form_valid(self, form):
        currency = form.save(commit=False)
        currency.user = self.request.user
        currency.save()
        return super(CurrencyCreate, self).form_valid(form)


class CurrencyUpdate(LoginRequiredMixin, MessageFormErrorsMixin,
    generic.UpdateView):
    model = Currency
    form_class = CurrencyForm

    @method_decorator(
        user_passes_test(lambda u: u.has_perm('money.change_currency')))
    def dispatch(self, request, *args, **kwargs):
        return super(CurrencyUpdate, self).dispatch(request, *args, **kwargs)

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


class CurrencyDelete(LoginRequiredMixin, generic.DeleteView):
    model = Currency

    @method_decorator(
        user_passes_test(lambda u: u.has_perm('money.delete_currency')))
    def dispatch(self, request, *args, **kwargs):
        return super(CurrencyDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Currency successfully deleted.'
        )
        return reverse('money:currency:list')


class TransactionList(LoginRequiredMixin, UserObjectsMixin, generic.ListView):
    model = Transaction


class TransactionDetail(LoginRequiredMixin, UserObjectsMixin,
    generic.DetailView):
    model = Transaction


class TransactionCreate(LoginRequiredMixin, UserObjectsMixin,
    MessageFormErrorsMixin,
    generic.CreateView):
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

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.save()
        return super(TransactionCreate, self).form_valid(form)


class TransactionDelete(LoginRequiredMixin, UserObjectsMixin,
    generic.DeleteView):
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


class WalletList(LoginRequiredMixin, UserObjectsMixin, generic.ListView):
    model = Wallet


class WalletDetail(LoginRequiredMixin, UserObjectsMixin, generic.DetailView):
    model = Wallet

    def get_context_data(self, **kwargs):
        context = super(WalletDetail, self).get_context_data(**kwargs)
        templates = self.object.templates
        transactions = self.object.transactions()
        context['templates'] = templates
        context['transactions'] = transactions
        return context


class WalletCreate(LoginRequiredMixin, UserObjectsMixin,
    MessageFormErrorsMixin,
    generic.CreateView):
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

    def form_valid(self, form):
        wallet = form.save(commit=False)
        wallet.user = self.request.user
        wallet.save()
        return super(WalletCreate, self).form_valid(form)


class WalletUpdate(LoginRequiredMixin, UserObjectsMixin,
    MessageFormErrorsMixin,
    generic.UpdateView):
    model = Wallet
    form_class = WalletForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Wallet successfully updated.'
        )
        return reverse('money:wallet:list')


class WalletDelete(LoginRequiredMixin, UserObjectsMixin, generic.DeleteView):
    model = Wallet
    form_class = WalletForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Wallet successfully deleted.'
        )
        return reverse('money:wallet:list')


class TemplateList(LoginRequiredMixin, UserObjectsMixin, generic.ListView):
    model = Template


class TemplateDetail(LoginRequiredMixin, UserObjectsMixin, generic.DetailView):
    model = Template


class TemplateCreate(LoginRequiredMixin, UserObjectsMixin,
    MessageFormErrorsMixin,
    generic.CreateView):
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

    def form_valid(self, form):
        template = form.save(commit=False)
        template.user = self.request.user
        template.save()
        return super(TemplateCreate, self).form_valid(form)


class TemplateUpdate(LoginRequiredMixin, UserObjectsMixin,
    MessageFormErrorsMixin,
    generic.UpdateView):
    model = Template
    form_class = TemplateForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Template successfully updated.'
        )
        return reverse('money:template:list')


class TemplateDelete(LoginRequiredMixin, UserObjectsMixin, generic.DeleteView):
    model = Template

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            'Template successfully deleted.'
        )
        return reverse('money:template:list')
