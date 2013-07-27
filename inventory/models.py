from django.db import models
from tax.models import TaxScheme
from ledger.models import Account


class Item(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=254)
    description = models.TextField(null=True)
    purchase_price = models.FloatField()
    purchase_account = models.ForeignKey(Account, related_name='purchase_items')
    purchase_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='purchase_items')
    sales_price = models.FloatField()
    sales_account = models.ForeignKey(Account, related_name='sales_items')
    sales_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='sales_items')