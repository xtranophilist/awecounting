from django.db import models
from tax.models import TaxScheme
from ledger.models import Account
from users.models import Company


class Category(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '[' + self.code + '] ' + self.name


class Item(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    purchase_price = models.FloatField()
    purchase_account = models.ForeignKey(Account, related_name='purchase_items')
    purchase_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='purchase_items')
    sales_price = models.FloatField()
    sales_account = models.ForeignKey(Account, related_name='sales_items')
    sales_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='sales_items')
    company = models.ForeignKey(Company)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return '[' + self.code + '] ' + self.name
