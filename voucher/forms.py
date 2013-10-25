from django import forms
from django.core.urlresolvers import reverse_lazy

from acubor.lib import KOModelForm, ExtFileField
from core.models import Currency
from ledger.models import Party
from voucher.models import Invoice, PurchaseVoucher, CashReceipt


class InvoiceForm(KOModelForm):
    party = forms.ModelChoiceField(Party.objects.all(), empty_label='Choose a customer',
                                   widget=forms.Select(attrs={'class': 'select2 placehold', 'data-field': 'Customer',
                                                              'data-add-url': reverse_lazy('create_party'),
                                   }),
                                   label='To')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None,
                                      widget=forms.Select(attrs={'class': 'select2'}))

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['party'].queryset = Party.objects.filter(company=company, customer_account__isnull=False)

    class Meta:
        model = Invoice
        exclude = ['company']


class PurchaseVoucherForm(KOModelForm):
    party = forms.ModelChoiceField(Party.objects.all(), empty_label=None,
                                   widget=forms.Select(attrs={'class': 'select2'}), label='From')
    currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None,
                                      widget=forms.Select(attrs={'class': 'select2'}))
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(PurchaseVoucherForm, self).__init__(*args, **kwargs)
        self.fields['party'].queryset = Party.objects.filter(company=company, supplier_account__isnull=False)

    class Meta:
        model = PurchaseVoucher
        exclude = ['company', 'pending_amount', 'total_amount']


class CashReceiptForm(KOModelForm):
    receipt_on = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))

    class Meta:
        model = CashReceipt
        exclude = ['company']