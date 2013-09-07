from django.db import models
from users.models import Company
from ledger.models import Account
from inventory.models import InventoryAccount


class DayJournal(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company)
    sales_tax = models.FloatField()
    cash_deposit = models.FloatField()
    cash_withdrawal = models.FloatField()
    cheque_deposit = models.FloatField()
    cash_actual = models.FloatField()

    def get_absolute_url(self):
        return '/day/' + str(self.date)

    def __str__(self):
        return self.company.name + '[' + str(self.date) + ']'

    class Meta:
        db_table = 'day_journal'


class CashSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-sales'


class CashPurchase(models.Model):
    sn = models.IntegerField()
    purchase_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_purchase')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-purchase'


class CashReceipt(models.Model):
    sn = models.IntegerField()
    received_from = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_receipt')


class CashPayment(models.Model):
    sn = models.IntegerField()
    payment_to = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_payment')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-payment'


class CreditSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account, related_name='sales_ledger')
    customer = models.ForeignKey(Account, related_name='customer')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_sales')


class CreditPurchase(models.Model):
    sn = models.IntegerField()
    purchase_ledger = models.ForeignKey(Account, related_name='purchase_ledger')
    supplier = models.ForeignKey(Account, related_name='supplier')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_purchase')


class CreditExpense(models.Model):
    sn = models.IntegerField()
    expense_head = models.ForeignKey(Account, related_name='expense_head')
    expense_claimed_by = models.ForeignKey(Account, related_name='expense_claimed_by')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_expense')


class CreditIncome(models.Model):
    sn = models.IntegerField()
    income_head = models.ForeignKey(Account, related_name='income_head')
    income_from = models.ForeignKey(Account, related_name='income_from')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_income')


class SummaryTransfer(models.Model):
    sn = models.IntegerField()
    transfer_type = models.ForeignKey(Account)
    cash = models.FloatField(blank=True, null=True)
    cheque = models.FloatField(blank=True, null=True)
    card = models.FloatField(blank=True, null=True)
    day_journal = models.ForeignKey(DayJournal, related_name='summary_transfer')


class CardSales(models.Model):
    amount = models.FloatField()
    commission_out = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='card_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-payment'


class CashEquivalentSales(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_equivalent_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-payment'


class ChequePurchase(models.Model):
    amount = models.FloatField()
    commission_in = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cheque_purchase')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '#cash-payment'


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


class LottoDetail(models.Model):
    sn = models.IntegerField()
    rate = models.FloatField()
    pack_count = models.IntegerField(default=1)
    day_open = models.IntegerField()
    day_close = models.IntegerField()
    addition = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='lotto_detail')


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