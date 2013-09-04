__author__ = 'xtranophilist'
import django_filters
from bank.models import BankCashDeposit, ChequePayment, ChequeDeposit
from acubor import filter_extra
from ledger.models import Account


class CashDepositFilter(django_filters.FilterSet):
    # invoice_no = django_filters.CharFilter(lookup_type='icontains')
    # date = filter_extra.DateRangeFilter(label='Date Range')
    # due_date = filter_extra.DateRangeFilter(label='Due Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(CashDepositFilter, self).__init__(*args, **kwargs)
        # self.filters['party'] = django_filters.ModelChoiceFilter(queryset=Party.objects.filter(company=company))

    class Meta:
        model = BankCashDeposit
        # fields = ['invoice_no', 'date', 'due_date', 'party', 'tax']


class ChequeDepositFilter(django_filters.FilterSet):
    # reference = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')
    clearing_date = filter_extra.DateRangeFilter(label='Clearing Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ChequeDepositFilter, self).__init__(*args, **kwargs)
        self.filters['bank_account'] = django_filters.ModelChoiceFilter(queryset=Account.objects.filter(company=company, category__name='Bank'))
        self.filters['benefactor'] = django_filters.ModelChoiceFilter(queryset=Account.objects.filter(company=company))

    class Meta:
        model = ChequeDeposit
        fields = ['bank_account', 'date', 'clearing_date', 'benefactor']


class ChequePaymentFilter(django_filters.FilterSet):
    # reference = django_filters.CharFilter(lookup_type='icontains')
    # date = filter_extra.DateRangeFilter(label='Date Range')
    # due_date = filter_extra.DateRangeFilter(label='Due Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ChequePaymentFilter, self).__init__(*args, **kwargs)
        # self.filters['party'] = django_filters.ModelChoiceFilter(queryset=Party.objects.filter(company=company))

    class Meta:
        model = ChequePayment
        # fields = ['reference', 'date', 'due_date', 'party', 'tax']