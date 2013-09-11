from django import forms
from mptt.forms import TreeNodeChoiceField

from acubor.lib import KOModelForm
from models import Account, Category, Party


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        self.scenario = kwargs.pop('scenario', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(company=self.company)
        # if self.scenario == 'Create':
        del self.fields['current_dr']
        del self.fields['current_cr']

    class Meta:
        model = Account
        exclude = ['company', 'parent']

    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data

        name = cleaned_data.get('name')
        code = cleaned_data.get('code')

        try:
            object = Account.objects.get(name=name, company=self.company)
            if not object.id == self.instance.id:
                raise forms.ValidationError("Account name already exists.")
        except Account.DoesNotExist:
            pass

        try:
            object = Account.objects.get(code=code, company=self.company)
            if not object.id == self.instance.id:
                raise forms.ValidationError("Account name already exists.")
        except Account.DoesNotExist:
            pass

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

        if Category.objects.filter(name=name, company=self.company).count() > 0:
            raise forms.ValidationError("Category name already exists.")

        # Always return the full collection of cleaned data.
        return cleaned_data