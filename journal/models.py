from django.db import models
from inventory.models import Item
from users.models import Company
from ledger.models import Account
from core.models import BankAccount
from tax.models import TaxScheme


class DayJournal(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company)

    class Meta:
        db_table = 'journal_day'


class DayCashSales(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField(blank=True, null=True)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_cash_sales')


class DayCashPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_cash_purchase')


class DayCashReceipt(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_cash_receipt')


class DayCashPayment(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_cash_payment')


class DayCreditSales(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_credit_sales')


class DayCreditPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_credit_purchase')


class DayCreditExpense(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_credit_expense')


class DayCreditIncome(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_credit_income')


class DaySummaryCash(models.Model):
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_summary_cash')


class DaySummaryEquivalent(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    inward = models.FloatField()
    outward = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_summary_equivalent')


class DaySummaryBank(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(BankAccount)
    collection = models.FloatField()
    withdrawal = models.FloatField()
    interest_receipt = models.FloatField()
    interest_and_commission = models.FloatField()
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_summary_bank')


class DaySummarySalesTax(models.Model):
    sn = models.IntegerField()
    tax_scheme = models.ForeignKey(TaxScheme)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_summary_sales_tax')


class DaySummaryInventory(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    purchase = models.FloatField()
    sales = models.FloatField()
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)
    day_journal = models.ForeignKey(DayJournal, related_name='day_summary_inventory')


class DayPayroll(models.Model):
    sn = models.IntegerField()
    head = models.CharField(max_length=254)
    total_taxable = models.FloatField()
    tax = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='day_payroll')