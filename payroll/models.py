from django.db import models
from ledger.models import Account
from users.models import Company


class Entry(models.Model):
    company = models.ForeignKey(Company)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class EntryRow(models.Model):
    sn = models.IntegerField()
    employee = models.ForeignKey(Account)
    pay_heading = models.CharField(max_length=254)
    amount = models.FloatField()
    hours = models.FloatField()
    tax = models.FloatField()
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    entry = models.ForeignKey(Entry)