from acubor.lib import KOModelForm
from django import forms
from models import Invoice, Currency


class InvoiceForm(KOModelForm):
    party = forms.CharField(widget=forms.TextInput(), label='To')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)
    date = forms.DateField(widget=KOModelForm.DateTypeInput())
    due_date = forms.DateField(widget=KOModelForm.DateTypeInput())

    class Meta:
        model = Invoice
