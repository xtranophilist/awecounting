from django import forms
from models import TaxScheme
from ledger.models import Account


class TaxSchemeForm(forms.ModelForm):
    class Meta:
        model = TaxScheme
        exclude = ['company']
