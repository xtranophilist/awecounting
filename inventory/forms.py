from acubor.lib import KOModelForm
from models import Item, Category
from ledger.models import Account
from tax.models import TaxScheme


class ItemForm(KOModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['purchase_account'].queryset = Account.objects.filter(company=company, category__name='Bank')
        self.fields['sales_account'].queryset = Account.objects.filter(company=company)
        self.fields['sales_tax_scheme'].queryset = TaxScheme.objects.filter(company=company)
        self.fields['category'].queryset = Category.objects.filter(company=company)

    class Meta:
        model = Item
        exclude = ['company', 'account']
