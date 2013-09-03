__author__ = 'xtranophilist'
import django_filters
from voucher.models import Invoice


class InvoiceFilter(django_filters.FilterSet):
    # invoice_no = django_filters.AllValuesFilter(widget=django_filters.widgets.LinkWidget)
    
    class Meta:
        model = Invoice
        fields = ['invoice_no']
