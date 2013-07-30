from acubor.lib import KOModelForm
from django import forms
from models import Invoice, Currency


class InvoiceForm(KOModelForm):
    # party = forms.CharField(widget=forms.TextInput(), label='To')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)
    date = forms.DateField(widget=KOModelForm.DateTypeInput(attrs={'class': 'date-picker'}))
    due_date = forms.DateField(widget=KOModelForm.DateTypeInput(attrs={'class': 'due-date'}))

    class Meta:
        model = Invoice
        exclude = ['company']
