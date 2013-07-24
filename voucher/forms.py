from acubor.lib import KOModelForm
from django import forms
from models import SalesVoucher


class SalesVoucherForm(KOModelForm):
    party = forms.CharField(widget=forms.TextInput(), label='To')

    class Meta:
        model = SalesVoucher
