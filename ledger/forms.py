from django import forms
from django.core.urlresolvers import reverse_lazy
from mptt.forms import TreeNodeChoiceField

from acubor.lib import KOModelForm
from acubor.lib import zero_for_none
from models import Account, Category, Party


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(Category.objects.all(), empty_label=None,
                                   widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Category',
                                                              'data-url': reverse_lazy(
                                                                  'create_category')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        self.scenario = kwargs.pop('scenario', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(company=self.company)
        # if self.scenario == 'Create':
        del self.fields['current_dr']
        del self.fields['current_cr']
        #if self.scenario == 'Update':
        #    del self.fields['opening_dr']
        #    del self.fields['opening_cr']

    class Meta:
        model = Account
        exclude = ['company', 'parent']

    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data

        name = cleaned_data.get('name')
        code = cleaned_data.get('code')
        opening_dr = cleaned_data.get('opening_dr')
        opening_cr = cleaned_data.get('opening_cr')

        if not zero_for_none(opening_dr) == 0 and not zero_for_none(opening_cr) == 0:
            raise forms.ValidationError("You can't enter both Opening Dr and Cr amounts.")

        try:
            object = Account.objects.get(name=name, company=self.company)
            if not object.id == self.instance.id:
                raise forms.ValidationError("Account name already exists.")
        except Account.DoesNotExist:
            pass

        try:
            object = Account.objects.get(code=code, company=self.company)
            if not object.id == self.instance.id:
                raise forms.ValidationError("Account code already exists.")
        except Account.DoesNotExist:
            pass

        # Always return the full collection of cleaned data.
        return cleaned_data


class PartyForm(KOModelForm):
    class Meta:
        model = Party
        exclude = ['company', 'customer_account', 'supplier_account']


class CategoryForm(KOModelForm):
    parent = TreeNodeChoiceField(Category.objects.all(), empty_label=None,
                                   widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Category',
                                                              'data-url': reverse_lazy(
                                                                  'create_category')}))


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