from acubor.lib import KOModelForm, ExtFileField
from django import forms
from core.models import Currency, Party
from voucher.models import Invoice, PurchaseVoucher


class InvoiceForm(KOModelForm):
    party = forms.ModelChoiceField(Party.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'select2'}))
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None,
                                      widget=forms.Select(attrs={'class': 'select2'}))

    class Meta:
        model = Invoice
        exclude = ['company']


class PurchaseVoucherForm(KOModelForm):
    party = forms.ModelChoiceField(Party.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'select2'}))
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None,
                                      widget=forms.Select(attrs={'class': 'select2'}))
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    class Meta:
        model = PurchaseVoucher
        exclude = ['company']
