from django.db import models
from inventory.models import Item
from ledger.models import Account
from tax.models import TaxScheme
from ledger.models import Party
from core.models import Currency
from users.models import Company


class Invoice(models.Model):
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    party = models.ForeignKey(Party, verbose_name=u'To')
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    invoice_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Currency)
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')
    company = models.ForeignKey(Company)

    class Meta:
        db_table = 'invoice'


class InvoiceParticular(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    description = models.TextField()
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', blank=True, null=True)
    invoice = models.ForeignKey(Invoice, related_name='particulars')

    class Meta:
        db_table = 'invoice_particular'


class PurchaseVoucher(models.Model):
    party = models.ForeignKey(Party, verbose_name=u'From')
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Currency)
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')
    attachment = models.FileField(upload_to='purchase_vouchers/%Y/%m/%d', blank=True, null=True)
    company = models.ForeignKey(Company)


class PurchaseParticular(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    description = models.TextField()
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', blank=True, null=True)
    purchase_voucher = models.ForeignKey(PurchaseVoucher, related_name='particulars')

    class Meta:
        db_table = 'purchase_particular'


class JournalVoucher(models.Model):
    voucher_no = models.CharField(max_length=10)
    date = models.DateField()
    company = models.ForeignKey(Company)


class JournalVoucherRow(models.Model):
    sn = models.IntegerField()
    dr_account = models.ForeignKey(Account, null=True, blank=True, related_name='dr_rows')
    cr_account = models.ForeignKey(Account, null=True, blank=True, related_name='cr_rows')
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    journal_voucher = models.ForeignKey(JournalVoucher, related_name='rows')


# class BankDetail(models.Model):
#     bank_account = models.ForeignKey(Account)
#     day = models.DateField()
#     company = models.ForeignKey(Company)
#
#
# class BankDetailRow(models.Model):
#     sn = models.IntegerField()
#     account = models.ForeignKey(Account)
#     type = models.CharField(max_length=3)
#     amount = models.FloatField()
#     bank_detail = models.ForeignKey(BankDetail, related_name='rows')
