from django.db import models
from ledger.models import Account
from users.models import Company


class Entry(models.Model):
    entry_no = models.CharField(max_length=10)
    company = models.ForeignKey(Company)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/payroll/' + str(self.id)


class EntryRow(models.Model):
    sn = models.IntegerField()
    employee = models.ForeignKey(Account)
    pay_heading = models.ForeignKey(Account, related_name='row')
    amount = models.FloatField()
    hours = models.FloatField()
    tax = models.FloatField()
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    entry = models.ForeignKey(Entry, related_name='rows')

    def get_absolute_url(self):
        return self.entry.get_absolute_url()