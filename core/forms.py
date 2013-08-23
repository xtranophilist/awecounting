from django import forms
from core.models import CompanySetting, Currency, Category
from ledger.models import Party
from acubor.lib import KOModelForm


class CompanySettingsForm(forms.ModelForm):
    default_currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)

    class Meta:
        model = CompanySetting
        exclude = ['company']


class PartyForm(KOModelForm):

    class Meta:
        model = Party
        exclude = ['company']


class TagForm(KOModelForm):
    class Meta:
        model = Category
        exclude = ['company']