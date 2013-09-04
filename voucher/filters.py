__author__ = 'xtranophilist'
import django_filters
from voucher.models import Invoice, PurchaseVoucher
from acubor import filter_extra
from ledger.models import Party


class InvoiceFilter(django_filters.FilterSet):
    invoice_no = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')
    due_date = filter_extra.DateRangeFilter(label='Due Date Range')
    party = django_filters.ModelChoiceFilter(queryset=Party.objects.all(), label='To')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InvoiceFilter, self).__init__(*args, **kwargs)
        if company:
            self.filters.queryset = Party.objects.filter(company=company)

    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'due_date', 'party', 'tax']


class PurchaseVoucherFilter(django_filters.FilterSet):
    reference = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')
    due_date = filter_extra.DateRangeFilter(label='Due Date Range')
    party = django_filters.ModelChoiceFilter(queryset=Party.objects.all(), label='From')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(PurchaseVoucherFilter, self).__init__(*args, **kwargs)
        if company:
            self.filters.queryset = Party.objects.filter(company=company)

    class Meta:
        model = PurchaseVoucher
        fields = ['reference', 'date', 'due_date', 'party', 'tax']