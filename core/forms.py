from django import forms
from core.models import CompanySetting, Currency, Party
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