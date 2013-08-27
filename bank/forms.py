from acubor.lib import KOModelForm
# from django import forms
from models import BankAccount, ChequeReceipt


class BankAccountForm(KOModelForm):

    class Meta:
        model = BankAccount
        exclude = ['company', 'account']


class ChequeReceiptForm(KOModelForm):
    class Meta:
        model = ChequeReceipt
        exclude = ['company']
