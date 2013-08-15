from django.db import models
from users.models import Company
from ledger.models import Account


class DayJournal(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/day/' + str(self.date)

    class Meta:
        db_table = 'day_journal'




class CashSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_sales')


class CashPurchase(models.Model):
    sn = models.IntegerField()
    purchase_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_purchase')


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
    inward = models.FloatField()
    outward = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_transfer')


class SummaryBank(models.Model):
    sn = models.IntegerField()
    bank_account = models.ForeignKey(Account)
    card_deposit = models.FloatField()
    cash_deposit = models.FloatField()
    account_transfer_plus = models.FloatField()
    account_transfer_minus = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_bank')


class SummarySalesTax(models.Model):
    sn = models.IntegerField()
    tax_scheme = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_sales_tax')


class SummaryInventory(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(Account)
    purchase = models.FloatField()
    sales = models.FloatField()
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_inventory')


# class Payroll(models.Model):
#     sn = models.IntegerField()
#     head = models.CharField(max_length=254)
#     total_taxable = models.FloatField()
#     tax = models.FloatField()
#     day_journal = models.ForeignKey(DayJournal, related_name='payroll')