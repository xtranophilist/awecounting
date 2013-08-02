from django.db import models
from inventory.models import Item
from users.models import Company
from ledger.models import Account
from core.models import BankAccount
from tax.models import TaxScheme


class DayCashSales(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    amount = models.FloatField()


class DayCashPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    amount = models.FloatField()


class DayCashReceipt(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    amount = models.FloatField()


class DayCashPayment(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()


class DayCreditSales(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()


class DayCreditPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()


class DayCreditExpense(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()


class DayCreditIncome(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()


class DaySummaryCash(models.Model):
    actual = models.FloatField()


class DaySummaryEquivalent(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    inward = models.FloatField()
    outward = models.FloatField()


class DaySummaryBank(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(BankAccount)
    collection = models.FloatField()
    withdrawal = models.FloatField()
    interest_receipt = models.FloatField()
    interest_and_commission = models.FloatField()
    actual = models.FloatField()


class DaySummarySalesTax(models.Model):
    sn = models.IntegerField()
    tax_scheme = models.ForeignKey(TaxScheme)
    amount = models.FloatField()


class DaySummaryInventory(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    purchase = models.FloatField()
    sales = models.FloatField()
    actual = models.FloatField()


class DayPayroll(models.Model):
    sn = models.IntegerField()
    head = models.CharField(max_length=254)
    total_taxable = models.FloatField()
    tax = models.FloatField()


class DayJournal(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company)
    day_cash_sales = models.ForeignKey(DayCashSales)
    day_cash_purchase = models.ForeignKey(DayCashPurchase)
    day_cash_receipt = models.ForeignKey(DayCashReceipt)
    day_cash_payment = models.ForeignKey(DayCashPayment)
    day_credit_sales = models.ForeignKey(DayCreditSales)
    day_credit_purchase = models.ForeignKey(DayCreditPurchase)
    day_credit_expense = models.ForeignKey(DayCreditExpense)
    day_credit_income = models.ForeignKey(DayCreditIncome)
    day_summary_cash = models.ForeignKey(DaySummaryCash)
    day_summary_equivalent = models.ForeignKey(DaySummaryEquivalent)
    day_summary_bank = models.ForeignKey(DaySummaryBank)
    day_summary_sales_tax = models.ForeignKey(DaySummarySalesTax)
    day_summary_inventory = models.ForeignKey(DaySummaryInventory)
    day_payroll = models.ForeignKey(DayPayroll)

    def __init__(self, *args, **kwargs):
        super(DayJournal, self).__init__(*args, **kwargs)
        self.day_cash_sales = DayCashSales()
        self.day_cash_purchase = DayCashPurchase()
        self.day_cash_receipt = DayCashReceipt()
        self.day_cash_payment = DayCashPayment()
        self.day_credit_sales = DayCreditSales()
        self.day_credit_purchase = DayCreditPurchase()
        self.day_credit_expense = DayCreditExpense()
        self.day_credit_income = DayCreditIncome()
        self.day_summary_cash = DaySummaryCash()
        self.day_summary_equivalent = DaySummaryEquivalent()
        self.day_summary_bank = DaySummaryBank()
        self.day_summary_sales_tax = DaySummarySalesTax()
        self.day_summary_inventory = DaySummaryInventory()
        self.day_payroll = DayPayroll()

    class Meta:
        db_table = 'journal_day'




