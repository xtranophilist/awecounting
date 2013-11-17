from django import forms
from django.core.urlresolvers import reverse_lazy

from acubor.lib import KOModelForm, ExtFileField
from core.models import Currency
from ledger.models import Party
from voucher.models import Invoice, PurchaseVoucher, CashReceipt


class InvoiceForm(KOModelForm):
    party = forms.ModelChoiceField(Party.objects.all(), empty_label='Choose a customer',
                                   widget=forms.Select(attrs={'class': 'select2 placehold', 'data-name': 'Customer',
                                                              'data-url': reverse_lazy('create_party'),
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
        exclude = ['company', 'status']


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
        self.company = kwargs.pop('company', None)
        super(PurchaseVoucherForm, self).__init__(*args, **kwargs)
        self.fields['party'].queryset = Party.objects.filter(company=self.company, supplier_account__isnull=False)

    def clean_voucher_no(self):
        try:
            existing = PurchaseVoucher.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested voucher no. has been provided!")
            return self.cleaned_data['voucher_no']
        except PurchaseVoucher.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = PurchaseVoucher
        exclude = ['company', 'pending_amount', 'total_amount', 'status']


class CashReceiptForm(KOModelForm):
    receipt_on = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))

    class Meta:
        model = CashReceipt
        exclude = ['company', 'status']