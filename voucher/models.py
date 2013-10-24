from django.db import models
from inventory.models import Item
from ledger.models import Account, Party
from tax.models import TaxScheme
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
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')
    pending_amount = models.FloatField()

    class Meta:
        db_table = 'invoice'
        unique_together = ('invoice_no', 'company')

    def get_voucher_no(self):
        return self.invoice_no


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

    def get_absolute_url(self):
        return '/voucher/invoice/' + self.invoice.invoice_no + '/'

    def get_voucher_no(self):
        return self.invoice.invoice_no

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

    def get_voucher_no(self):
        return self.id


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

    def get_absolute_url(self):
        return '/voucher/purchase/' + str(self.purchase_voucher.id) + '/'

    def get_voucher_no(self):
        return self.purchase_voucher.id

    class Meta:
        db_table = 'purchase_particular'


class JournalVoucher(models.Model):
    voucher_no = models.CharField(max_length=10)
    date = models.DateField()
    company = models.ForeignKey(Company)
    narration = models.TextField()

    def get_voucher_no(self):
        return self.voucher_no


class JournalVoucherRow(models.Model):
    types = [('Dr', 'Dr'), ('Cr', 'Dr')]
    type = models.CharField(choices=types, default='Dr', max_length=2)
    account = models.ForeignKey(Account, related_name='account_rows')
    description = models.TextField()
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    journal_voucher = models.ForeignKey(JournalVoucher, related_name='rows')

    def get_absolute_url(self):
        return '/voucher/journal/' + str(self.journal_voucher_id)

    def get_voucher_no(self):
        return self.journal_voucher.voucher_no


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


class CashReceipt(models.Model):
    party = models.ForeignKey(Party)
    receipt_on = models.DateField()
    reference = models.CharField(max_length=50)
    amount = models.FloatField()
    description = models.TextField()
    company = models.ForeignKey(Company)


class CashReceiptRow(models.Model):
    invoice = models.ForeignKey(Invoice)
    receipt = models.FloatField()
    discount = models.FloatField()
    cash_receipt = models.ForeignKey(CashReceipt, related_name='rows')