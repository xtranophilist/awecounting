from acubor.lib import KOModelForm
# from django import forms
from models import Account, Category, Party
from mptt.forms import TreeNodeChoiceField


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Account
        exclude = ['company', 'parent']


class PartyForm(KOModelForm):

    class Meta:
        model = Party
        exclude = ['company']


class CategoryForm(KOModelForm):
    class Meta:
        model = Category
        exclude = ['company']