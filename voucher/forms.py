from django import forms
from models import SalesVoucher

class SalesVoucherForm(forms.ModelForm):

    class Meta:
        model = SalesVoucher
