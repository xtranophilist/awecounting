__author__ = 'xtranophilist'
import django_filters
from voucher.models import Invoice
from acubor import filter_extra
from ledger.models import Party


class InvoiceFilter(django_filters.FilterSet):
    invoice_no = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InvoiceFilter, self).__init__(*args, **kwargs)
        self.filters['party'] = django_filters.ModelChoiceFilter(queryset=Party.objects.filter(company=company))

    class Meta:
        model = Invoice
        fields = ['invoice_no', 'date', 'party']