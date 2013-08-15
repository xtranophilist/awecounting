from acubor.lib import KOModelForm
from django import forms
from models import Account


class AccountForm(KOModelForm):

    class Meta:
        model = Account
        exclude = ['company']

