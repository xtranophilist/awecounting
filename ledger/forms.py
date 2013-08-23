from acubor.lib import KOModelForm
# from django import forms
from models import Account, BankAccount, Category
from mptt.forms import TreeNodeChoiceField


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Account
        exclude = ['company', 'parent']


class BankAccountForm(KOModelForm):

    class Meta:
        model = BankAccount
        exclude = ['company', 'account']

