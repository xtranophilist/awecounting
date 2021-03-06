from django import forms
from core.models import CompanySetting, Currency, VoucherSetting


class CompanySettingsForm(forms.ModelForm):
    default_currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)

    class Meta:
        model = CompanySetting
        exclude = ['company', 'default_dayjournal']


class VoucherSettingsForm(forms.ModelForm):
    class Meta:
        model = VoucherSetting
        exclude = ['company']
