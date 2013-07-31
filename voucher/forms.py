from acubor.lib import KOModelForm
from django import forms
from core.models import Currency
from voucher.models import Invoice, PurchaseVoucher


class InvoiceForm(KOModelForm):
    # party = forms.CharField(widget=forms.TextInput(), label='To')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)
    date = forms.DateField(widget=KOModelForm.DateTypeInput(attrs={'class': 'date-picker'}))
    due_date = forms.DateField(widget=KOModelForm.DateTypeInput(attrs={'class': 'due-date'}))

    class Meta:
        model = Invoice
        exclude = ['company']


class PurchaseVoucherForm(KOModelForm):
    # party = forms.CharField(widget=forms.TextInput(), label='To')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None)
    date = forms.DateField(widget=KOModelForm.DateTypeInput(attrs={'class': 'date-picker'}))
    due_date = forms.DateField(widget=KOModelForm.DateTypeInput(attrs={'class': 'due-date'}))
    attachment = forms.FileField(
        label='Add an attachment',
        help_text='',
        required=False,
    )

    class Meta:
        model = PurchaseVoucher
        exclude = ['company']
