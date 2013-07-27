from acubor.lib import KOModelForm
from django import forms
from models import SalesVoucher, Currency


class SalesVoucherForm(KOModelForm):
    party = forms.CharField(widget=forms.TextInput(), label='To')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)
    invoice_no = forms.CharField(
               widget=forms.TextInput(attrs={'maxlength': 5, 'size': 5}))


    class Meta:
        model = SalesVoucher
