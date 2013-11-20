from django.db import models
from acubor.lib import get_next_voucher_no
from inventory.models import Item
from ledger.models import Account, Party
from tax.models import TaxScheme
from core.models import Currency
from users.models import Company


class Invoice(models.Model):
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    party = models.ForeignKey(Party, verbose_name=u'To', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    voucher_no = models.IntegerField(verbose_name='Invoice No.')
    reference = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, blank=True)
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive', null=True, blank=True)
    company = models.ForeignKey(Company)
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')
    pending_amount = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'invoice'
        #unique_together = ('invoice_no', 'company')

    def get_voucher_no(self):
        return self.invoice_no

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Invoice, self.company)

        #def total_amount(self):
        #    total = 0;
        #    for particular in self.particulars:


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
    voucher_no = models.IntegerField()
    party = models.ForeignKey(Party, verbose_name=u'From', null=True)
    date = models.DateField(null=True)
    due_date = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Currency)
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')
    attachment = models.FileField(upload_to='purchase_vouchers/%Y/%m/%d', blank=True, null=True)
    company = models.ForeignKey(Company)
    pending_amount = models.FloatField(null=True)
    total_amount = models.FloatField(null=True)
    description = models.TextField(null=True, blank=True)
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(PurchaseVoucher, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(PurchaseVoucher, self.company)

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
    #voucher_no = models.CharField(max_length=10)
    voucher_no = models.IntegerField()
    date = models.DateField()
    company = models.ForeignKey(Company)
    narration = models.TextField()
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def get_voucher_no(self):
        return self.voucher_no

    def __init__(self, *args, **kwargs):
        super(JournalVoucher, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(JournalVoucher, self.company)


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
    voucher_no = models.IntegerField()
    party = models.ForeignKey(Party, verbose_name='Receipt From')
    receipt_on = models.DateField()
    reference = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(CashReceipt, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(CashReceipt, self.company)


class CashReceiptRow(models.Model):
    invoice = models.ForeignKey(Invoice)
    receipt = models.FloatField()
    discount = models.FloatField()
    cash_receipt = models.ForeignKey(CashReceipt, related_name='rows')


class CashPayment(models.Model):
    voucher_no = models.IntegerField()
    party = models.ForeignKey(Party, verbose_name='Paid To')
    payment_on = models.DateField()
    reference = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(CashPayment, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(CashPayment, self.company)


class CashPaymentRow(models.Model):
    purchase_voucher = models.ForeignKey(PurchaseVoucher)
    payment = models.FloatField()
    discount = models.FloatField()
    cash_payment = models.ForeignKey(CashPayment, related_name='rows')


class FixedAsset(models.Model):
    from_account = models.ForeignKey(Account)
    voucher_no = models.IntegerField()
    date = models.DateField()
    reference = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(FixedAsset, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(FixedAsset, self.company)


class FixedAssetRow(models.Model):
    asset_ledger = models.ForeignKey(Account)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    fixed_asset = models.ForeignKey(FixedAsset, related_name='rows')


class AdditionalDetail(models.Model):
    assets_code = models.CharField(max_length=100, null=True, blank=True)
    assets_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_name = models.CharField(max_length=100, null=True, blank=True)
    vendor_address = models.CharField(max_length=254, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    useful_life = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    warranty_period = models.CharField(max_length=100, null=True, blank=True)
    maintenance = models.CharField(max_length=100, null=True, blank=True)
    fixed_asset = models.ForeignKey(FixedAsset, related_name='additional_details')