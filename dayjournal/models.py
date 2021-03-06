from django.db import models
from users.models import Company
from ledger.models import Account
from inventory.models import InventoryAccount

from acubor.lib import get_next_voucher_no


class DayJournal(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    company = models.ForeignKey(Company)
    cash_deposit = models.FloatField()
    cash_withdrawal = models.FloatField()
    cheque_deposit = models.FloatField()
    cash_actual = models.FloatField()
    lotto_sales_dispenser_amount = models.FloatField(default=0)
    lotto_sales_register_amount = models.FloatField(default=0)
    scratch_off_sales_register_amount = models.FloatField(default=0)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Approved')
    register_sales_amount = models.FloatField(default=0)
    register_sales_tax = models.FloatField(default=0)
    scratch_off_sales_manual = models.FloatField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(DayJournal, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(DayJournal, self.company)

    def get_absolute_url(self):
        return '/day/' + str(self.date)

    def __str__(self):
        return self.company.name + '[' + str(self.date) + ']'

    class Meta:
        db_table = 'day_journal'
        unique_together = ('voucher_no', 'company')


class CashSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-sales'


class SummaryTransfer(models.Model):
    sn = models.IntegerField()
    transfer_type = models.ForeignKey(Account)
    cash = models.FloatField(blank=True, null=True)
    cheque = models.FloatField(blank=True, null=True)
    card = models.FloatField(blank=True, null=True)
    day_journal = models.ForeignKey(DayJournal, related_name='summary_transfer')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#summary-transfer'


class CardSales(models.Model):
    amount = models.FloatField()
    commission_out = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='card_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#card-sales'


class CashEquivalentSales(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_equivalent_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-equivalent-sales'


class SummaryInventory(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(InventoryAccount)
    purchase = models.IntegerField()
    sales = models.IntegerField()
    actual = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_inventory')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#summary-inventory'


class InventoryFuel(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(InventoryAccount)
    purchase = models.IntegerField()
    sales = models.IntegerField()
    actual = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='inventory_fuel')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#inventory-fuel'


#Name changed to Scratch Off
class LottoDetail(models.Model):
    sn = models.IntegerField()
    rate = models.FloatField()
    pack_count = models.IntegerField(default=1)
    day_open = models.IntegerField()
    day_close = models.IntegerField()
    addition = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='lotto_detail')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#lotto-detail'


class SalesAttachment(models.Model):
    attachment = models.FileField(upload_to='day_sales_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='sales_attachments')


class PurchaseAttachment(models.Model):
    attachment = models.FileField(upload_to='day_purchase_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='purchase_attachments')


class BankAttachment(models.Model):
    attachment = models.FileField(upload_to='day_bank_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='bank_attachments')


class OtherAttachment(models.Model):
    attachment = models.FileField(upload_to='day_other_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='other_attachments')


class VendorPayout(models.Model):
    sn = models.IntegerField()
    vendor = models.ForeignKey(Account, related_name="vendor_payouts")
    amount = models.FloatField()
    purchase_ledger = models.ForeignKey(Account, related_name='payouts', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    paid = models.ForeignKey(Account)
    choices = [('new', 'New Purchase'), ('old', 'Old Bill Payment'), ('settlement', 'Account Settlement'),
               ('payment', 'Advance Payment')]
    type = models.CharField(max_length=10, choices=choices, default='new')
    day_journal = models.ForeignKey(DayJournal, related_name='vendor_payout')


class OtherPayout(models.Model):
    sn = models.IntegerField()
    paid_to = models.ForeignKey(Account, related_name='paid_for')
    amount = models.FloatField()
    remarks = models.TextField(null=True, blank=True)
    paid = models.ForeignKey(Account)
    day_journal = models.ForeignKey(DayJournal, related_name='other_payout')