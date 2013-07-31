from django.db import models
from inventory.models import Item
from ledger.models import Account
from tax.models import TaxScheme
from core.models import Party, Currency
from users.models import Company


class Invoice(models.Model):
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    party = models.ForeignKey(Party, verbose_name=u'To')
    date = models.DateField()
    due_date = models.DateField(null=True)
    invoice_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, null=True)
    currency = models.ForeignKey(Currency)
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')
    company = models.ForeignKey(Company)

    class Meta:
        db_table = 'invoice'


class Particular(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    description = models.TextField()
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField()
    discount = models.FloatField()
    account = models.ForeignKey(Account)
    tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate')
    invoice = models.ForeignKey(Invoice, related_name='particulars')


class PurchaseVoucher(models.Model):
    party = models.ForeignKey(Party, verbose_name=u'From')
    date = models.DateField()
    due_date = models.DateField(null=True)
    # invoice_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, null=True)
    currency = models.ForeignKey(Currency)
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')
    attachment = models.FileField(upload_to='pv/%Y/%m/%d', blank=True, null=True)
    company = models.ForeignKey(Company)
