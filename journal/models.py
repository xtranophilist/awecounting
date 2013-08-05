from django.db import models
from inventory.models import Item
from users.models import Company
from ledger.models import Account
from core.models import BankAccount
from tax.models import TaxScheme


class DayJournal(models.Model):
    date = models.DateField()
    company = models.ForeignKey(Company)
    # day_cash_sales = models.ManyToManyField(DayCashSales)
    # day_cash_purchase = models.ManyToManyField(DayCashPurchase)
    # day_cash_receipt = models.ManyToManyField(DayCashReceipt)
    # day_cash_payment = models.ManyToManyField(DayCashPayment)
    # day_credit_sales = models.ManyToManyField(DayCreditSales)
    # day_credit_purchase = models.ManyToManyField(DayCreditPurchase)
    # day_credit_expense = models.ManyToManyField(DayCreditExpense)
    # day_credit_income = models.ManyToManyField(DayCreditIncome)
    # day_summary_equivalent = models.ManyToManyField(DaySummaryEquivalent)
    # day_summary_bank = models.ManyToManyField(DaySummaryBank)
    # day_summary_sales_tax = models.ManyToManyField(DaySummarySalesTax)
    # day_summary_inventory = models.ManyToManyField(DaySummaryInventory)
    # day_payroll = models.ManyToManyField(DayPayroll)
    # day_summary_cash = models.ForeignKey(DaySummaryCash)

    # def __init__(self, *args, **kwargs):
    #     super(DayJournal, self).__init__(*args, **kwargs)
    #     if self.pk is None:
            # self.day_cash_sales = DayCashSales()
            # self.day_cash_purchase = DayCashPurchase()
            # self.day_cash_receipt = DayCashReceipt()
            # self.day_cash_payment = DayCashPayment()
            # self.day_credit_sales = DayCreditSales()
            # self.day_credit_purchase = DayCreditPurchase()
            # self.day_credit_expense = DayCreditExpense()
            # self.day_credit_income = DayCreditIncome()
            # self.day_summary_cash = DaySummaryCash()
            # self.day_summary_equivalent = DaySummaryEquivalent()
            # self.day_summary_bank = DaySummaryBank()
            # self.day_summary_sales_tax = DaySummarySalesTax()
            # self.day_summary_inventory = DaySummaryInventory()
            # self.day_payroll = DayPayroll()

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
    day_journal = models.ForeignKey(DayJournal)


class DayCashPayment(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DayCreditSales(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DayCreditPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DayCreditExpense(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DayCreditIncome(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DaySummaryCash(models.Model):
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DaySummaryEquivalent(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    inward = models.FloatField()
    outward = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DaySummaryBank(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(BankAccount)
    collection = models.FloatField()
    withdrawal = models.FloatField()
    interest_receipt = models.FloatField()
    interest_and_commission = models.FloatField()
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DaySummarySalesTax(models.Model):
    sn = models.IntegerField()
    tax_scheme = models.ForeignKey(TaxScheme)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DaySummaryInventory(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    purchase = models.FloatField()
    sales = models.FloatField()
    actual = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)


class DayPayroll(models.Model):
    sn = models.IntegerField()
    head = models.CharField(max_length=254)
    total_taxable = models.FloatField()
    tax = models.FloatField()
    day_journal = models.ForeignKey(DayJournal)