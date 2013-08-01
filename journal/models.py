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
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCashPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCashReceipt(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCashPayment(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCreditSales(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCreditPurchase(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    quantity = models.FloatField()
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCreditExpense(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DayCreditIncome(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DaySummaryCash(models.Model):
    actual = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


class DaySummaryEquivalent(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    inward = models.FloatField()
    outward = models.FloatField()
    date = models.DateField()
    company = models.ForeignKey(Company)


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
