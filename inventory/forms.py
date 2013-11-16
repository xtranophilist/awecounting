from django import forms
from django.core.urlresolvers import reverse_lazy
from mptt.forms import TreeNodeChoiceField

from acubor.lib import KOModelForm
from models import Item, Category, Unit
from ledger.models import Account, Category as AccountCategory
from tax.models import TaxScheme


class ItemForm(KOModelForm):
    category = TreeNodeChoiceField(Category.objects.all(), empty_label=None,
                                   widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Category',
                                                              'data-url': reverse_lazy(
                                                                  'create_inventory_category')}))
    purchase_tax_scheme = forms.ModelChoiceField(TaxScheme.objects.all(), empty_label=None,
                                                 widget=forms.Select(
                                                     attrs={'class': 'select2', 'data-name': 'Tax Scheme',
                                                            'data-url': reverse_lazy('create_tax_scheme')}))
    sales_tax_scheme = forms.ModelChoiceField(TaxScheme.objects.all(), empty_label=None,
                                              widget=forms.Select(
                                                  attrs={'class': 'select2', 'data-name': 'Tax Scheme',
                                                         'data-url': reverse_lazy('create_tax_scheme')}))
    purchase_account = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                              widget=forms.Select(
                                                  attrs={'class': 'select2', 'data-name': 'Purchase Account'}))
    sales_account = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                           widget=forms.Select(
                                               attrs={'class': 'select2', 'data-name': 'Sales Account'}))

    unit = forms.ModelChoiceField(Unit.objects.all(), empty_label=None,
                                  widget=forms.Select(
                                      attrs={'class': 'select2', 'data-name': 'Unit',
                                             'data-url': reverse_lazy('create_unit')}))


    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['purchase_account'].queryset = Account.objects.filter(company=company, category__name='Purchase')
        self.fields['purchase_tax_scheme'].queryset = TaxScheme.objects.filter(company=company)
        self.fields['sales_account'].queryset = Account.objects.filter(company=company, category__name='Sales')
        self.fields['sales_tax_scheme'].queryset = TaxScheme.objects.filter(company=company)
        self.fields['category'].queryset = Category.objects.filter(company=company)
        self.fields['purchase_account'].widget.attrs['data-url'] = reverse_lazy(
            'create_account') + '?category_id=' + str(AccountCategory.objects.get(name='Purchase', company=company).id)
        self.fields['sales_account'].widget.attrs['data-url'] = reverse_lazy(
            'create_account') + '?category_id=' + str(AccountCategory.objects.get(name='Sales', company=company).id)
        self.fields['unit'].queryset = Unit.objects.filter(company=company)


    class Meta:
        model = Item
        exclude = ['company', 'account', 'sales_price', 'purchase_price']


class CategoryForm(KOModelForm):
    parent = TreeNodeChoiceField(Category.objects.all(),
                                 widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Category',
                                                            'data-url': reverse_lazy(
                                                                'create_inventory_category')}))

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


class UnitForm(KOModelForm):
    class Meta:
        model = Unit
        exclude = ['company']