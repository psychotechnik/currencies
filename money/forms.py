from django import forms
from money.models import Currency, Transaction, Wallet, Template

class CurrencyForm(forms.ModelForm):
    title = forms.CharField(label='', required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Currency title'}))
    code = forms.CharField(label='', required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Currency code'}))

    class Meta:
        model = Currency


class TransactionForm(forms.ModelForm):
    template = forms.ModelChoiceField(queryset=Template.objects.all(),
        label='', empty_label='Choice template', required=True,
        widget=forms.Select(attrs={'class': 'span3'}))
    rate = forms.FloatField(label='', initial=1.0,
        widget=forms.TextInput(
            attrs={'placeholder': 'Rate', 'class': 'span2'}))
    source_amount = forms.FloatField(label='', min_value=0.01,
        widget=forms.TextInput(
            attrs={'placeholder': 'Amount', 'class': 'span2'}))

    class Meta:
        model = Transaction
        fields = (
            'template',
            'rate',
            'source_amount'
            )

    def clean_source_amount(self):
        template = self.cleaned_data.get('template')
        source_amount = self.cleaned_data.get('source_amount')
        if template.source:
            if source_amount > template.source.balance:
                raise forms.ValidationError('Source balance limit is exceeded.')
        return source_amount



class WalletForm(forms.ModelForm):
    title = forms.CharField(label='',
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'span4'}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
        label='', empty_label='Choice currency',
        widget=forms.Select(attrs={'class': 'span3'}))

    class Meta:
        model = Wallet
        fields = (
            'title',
            'currency',
            )


class TemplateForm(forms.ModelForm):
    title = forms.CharField(label='',
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'span3'}))
    source = forms.ModelChoiceField(queryset=Wallet.objects.all(),
        label='', required=False, empty_label='Source',
        widget=forms.Select(attrs={'class': 'span2'}))
    destination = forms.ModelChoiceField(queryset=Wallet.objects.all(),
        label='', required=False, empty_label='Destination',
        widget=forms.Select(attrs={'class': 'span2'}))

    class Meta:
        model = Template
        fields = (
            'title',
            'source',
            'destination',
            )

    def clean(self):
        cleaned_data = super(TemplateForm, self).clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')
        if not source and not destination:
            raise forms.ValidationError(
                'Source and destination can not be empty.'
            )
        if source == destination:
            raise forms.ValidationError(
                'This template does not make sense.'
            )
        try:
            Template.objects.get(source=source, destination=destination)
            raise forms.ValidationError(
                'Template already exists.'
            )
        except Template.DoesNotExist:
            pass
        return cleaned_data
