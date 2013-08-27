from acubor.lib import KOModelForm
# from django import forms
from models import BankAccount


class BankAccountForm(KOModelForm):

    class Meta:
        model = BankAccount
        exclude = ['company', 'account']

