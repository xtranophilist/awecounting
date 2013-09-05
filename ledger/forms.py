from django import forms
from mptt.forms import TreeNodeChoiceField

from acubor.lib import KOModelForm
from models import Account, Category, Party


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(company=self.company)

    class Meta:
        model = Account
        exclude = ['company', 'parent']

    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data

        name = cleaned_data.get('name')
        code = cleaned_data.get('code')

        if Account.objects.filter(name=name, company=self.company).count() > 0:
            raise forms.ValidationError("Account name already exists.")

        if Account.objects.filter(code=code, company=self.company).count() > 0:
            raise forms.ValidationError("Account code already exists.")

        # Always return the full collection of cleaned data.
        return cleaned_data


class PartyForm(KOModelForm):
    class Meta:
        model = Party
        exclude = ['company']


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

        print 111

        print Category.objects.filter(name=name, company=self.company)

        if Category.objects.filter(name=name, company=self.company).count() > 0:
            raise forms.ValidationError("Category name already exists.")

        # Always return the full collection of cleaned data.
        return cleaned_data