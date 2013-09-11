from django import forms
from mptt.forms import TreeNodeChoiceField

from acubor.lib import KOModelForm
from models import Item, Category
from ledger.models import Account
from tax.models import TaxScheme


class ItemForm(KOModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['purchase_account'].queryset = Account.objects.filter(company=company, category__name='Purchase')
        self.fields['purchase_tax_scheme'].queryset = TaxScheme.objects.filter(company=company)
        self.fields['sales_account'].queryset = Account.objects.filter(company=company, category__name='Sales')
        self.fields['sales_tax_scheme'].queryset = TaxScheme.objects.filter(company=company)
        self.fields['category'].queryset = Category.objects.filter(company=company)

    class Meta:
        model = Item
        exclude = ['company', 'account', 'sales_price', 'purchase_price']


class CategoryForm(KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(company=self.company)

    class Meta:
        model = Category
        exclude = ['company']

    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data

        name = cleaned_data.get('name')

        if Category.objects.filter(name=name, company=self.company).count() > 0:
            raise forms.ValidationError("Category name already exists.")

        # Always return the full collection of cleaned data.
        return cleaned_data