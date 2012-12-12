from django import forms
from money.models import Currency, Transaction, Wallet, Template

class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency


class TransactionForm(forms.ModelForm):

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

    class Meta:
        model = Wallet
        fields = (
            'title',
            'currency',
            )


class TemplateForm(forms.ModelForm):

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
