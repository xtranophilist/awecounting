from acubor.lib import KOModelForm
# from django import forms
from models import Account, BankAccount


class AccountForm(KOModelForm):

    class Meta:
        model = Account
        exclude = ['company', 'parent']


class BankAccountForm(KOModelForm):

    class Meta:
        model = BankAccount
        exclude = ['company', 'account']

