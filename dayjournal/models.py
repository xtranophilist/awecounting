from django.db import models
from users.models import Company
from ledger.models import Account, Transaction
from inventory.models import InventoryAccount

class DayJournal(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company)
    sales_tax = models.FloatField()

    def get_absolute_url(self):
        return '/day/' + str(self.date)

    def __str__(self):
        return self.date

    class Meta:
        db_table = 'day_journal'


class CashSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_sales')
    transactions = models.ManyToManyField(Transaction)


class CashPurchase(models.Model):
    sn = models.IntegerField()
    purchase_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_purchase')
    transaction = models.ForeignKey(Transaction)


class CashReceipt(models.Model):
    sn = models.IntegerField()
    received_from = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_receipt')
    transaction = models.ForeignKey(Transaction)


class CashPayment(models.Model):
    sn = models.IntegerField()
    payment_to = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_payment')
    transaction = models.ForeignKey(Transaction)


class CreditSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account, related_name='sales_ledger')
    customer = models.ForeignKey(Account, related_name='customer')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_sales')
    transaction = models.ForeignKey(Transaction)


class CreditPurchase(models.Model):
    sn = models.IntegerField()
    purchase_ledger = models.ForeignKey(Account, related_name='purchase_ledger')
    supplier = models.ForeignKey(Account, related_name='supplier')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_purchase')
    transaction = models.ForeignKey(Transaction)


class CreditExpense(models.Model):
    sn = models.IntegerField()
    expense_head = models.ForeignKey(Account, related_name='expense_head')
    expense_claimed_by = models.ForeignKey(Account, related_name='expense_claimed_by')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_expense')
    transaction = models.ForeignKey(Transaction)


class CreditIncome(models.Model):
    sn = models.IntegerField()
    income_head = models.ForeignKey(Account, related_name='income_head')
    income_from = models.ForeignKey(Account, related_name='income_from')
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='credit_income')
    transaction = models.ForeignKey(Transaction)


class SummaryCash(models.Model):
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_cash')


class SummaryEquivalent(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(Account)
    inward = models.FloatField()
    outward = models.FloatField()
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_equivalent')


class SummaryTransfer(models.Model):
    sn = models.IntegerField()
    transfer_type = models.ForeignKey(Account)
    cash = models.FloatField(blank=True, null=True)
    cheque = models.FloatField(blank=True, null=True)
    card = models.FloatField(blank=True, null=True)
    day_journal = models.ForeignKey(DayJournal, related_name='summary_transfer')


class SummaryBank(models.Model):
    sn = models.IntegerField()
    bank_account = models.ForeignKey(Account)
    cheque_deposit = models.FloatField()
    cash_deposit = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_bank')


# class SummarySalesTax(models.Model):
#     sn = models.IntegerField()
#     tax_scheme = models.ForeignKey(Account)
#     amount = models.FloatField()
#     day_journal = models.ForeignKey(DayJournal, related_name='summary_sales_tax')


# class SummaryInventory(models.Model):
#     sn = models.IntegerField()
#     particular = models.ForeignKey(Account)
#     purchase = models.FloatField()
#     sales = models.FloatField()
#     actual = models.FloatField()
#     day_journal = models.ForeignKey(DayJournal, related_name='summary_inventory')


class SummaryLotto(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(Account)
    disp = models.FloatField()
    reg = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_lotto')


# class SummaryUtility(models.Model):
#     amount = models.FloatField()
#     day_journal = models.ForeignKey(DayJournal, related_name='summary_utility')


class SummaryInventory(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(InventoryAccount)
    # opening = models.IntegerField()
    purchase = models.IntegerField()
    sales = models.IntegerField()
    actual = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_inventory')


# class LottoDetail(models.Model):
#     company = models.ForeignKey(Company)
#     date = models.DateField()


class LottoDetailRow(models.Model):
    sn = models.IntegerField()
    type = models.ForeignKey(Account, null=True, blank=True)
    rate = models.FloatField()
    purchase_pack = models.IntegerField(default=1)
    purchase_quantity = models.IntegerField()
    sold_quantity = models.IntegerField()
    actual_quantity = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='lotto_details')


class CardSales(models.Model):
    amount = models.FloatField()
    commission_out = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='card_sales')
