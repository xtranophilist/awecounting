from django.db import models
from inventory.models import Item
from ledger.models import Account
from tax.models import TaxScheme


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    fax = models.CharField(max_length=20)


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    latest_usd_rate = models.FloatField()

    class Meta:
        verbose_name_plural = u'Currencies'

    def __unicode__(self):
        return self.code


class SalesVoucher(models.Model):
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    party = models.ForeignKey(Party, verbose_name=u'To')
    date = models.DateField()
    due_date = models.DateField(null=True)
    invoice_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, null=True)
    currency = models.ForeignKey(Currency)
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')


class Particular(models.Model):
    item = models.ForeignKey(Item)
    description = models.TextField()
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField()
    discount = models.FloatField()
    account = models.ForeignKey(Account)
    tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate')
    sales_voucher = models.ForeignKey(SalesVoucher, related_name='particulars')


class PurchaseVoucher(models.Model):
    party = models.ForeignKey(Party, verbose_name=u'From')
    date = models.DateField()
    due_date = models.DateField(null=True)
    invoice_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, null=True)
    currency = models.ForeignKey(Currency)
    tax = models.CharField(max_length=10)
