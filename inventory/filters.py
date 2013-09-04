import django_filters
from inventory.models import InventoryAccount, Item
from acubor import filter_extra
from ledger.models import Account


class InventoryItemFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_type='icontains')
    name = django_filters.CharFilter(lookup_type='icontains')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InventoryItemFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Item
        fields = ['code', 'name', 'sales_tax_scheme', 'category']


class InventoryAccountFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InventoryAccount, self).__init__(*args, **kwargs)
        # self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        # self.filters['benefactor'].field.queryset = Account.objects.filter(company=company)

    class Meta:
        model = InventoryAccount


        # class CashDepositFilter(django_filters.FilterSet):
        #     cheque_number = django_filters.CharFilter(lookup_type='icontains')
        #     date = filter_extra.DateRangeFilter(label='Date Range')
        #
        #     def __init__(self, *args, **kwargs):
        #         company = kwargs.pop('company', None)
        #         super(CashDepositFilter, self).__init__(*args, **kwargs)
        #         self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        #         self.filters['benefactor'].field.queryset = Account.objects.filter(company=company)
        #
        #     class Meta:
        #         model = BankCashDeposit
        #         fields = ['bank_account', 'date', 'benefactor', 'amount']