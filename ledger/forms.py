from acubor.lib import KOModelForm
# from django import forms
from models import Account, Category, Party
from mptt.forms import TreeNodeChoiceField


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(company=company)

    class Meta:
        model = Account
        exclude = ['company', 'parent']


class PartyForm(KOModelForm):
    class Meta:
        model = Party
        exclude = ['company']


class CategoryForm(KOModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(company=company)

    class Meta:
        model = Category
        exclude = ['company']