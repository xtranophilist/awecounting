from django.db import models
from users.models import Company


class Account(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    current_balance = models.FloatField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

    def get_absolute_url(self):
        return '/account/' + str(self.id)

    def __unicode__(self):
        return self.name


class InventoryAccount(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    date = models.DateField()
    amount = models.FloatField()
    current_balance = models.FloatField()
    type = models.CharField(max_length=2)  # Dr. or Cr.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, null=True, blank=True)
    accounts = models.ManyToManyField(Account, related_name='tags', blank=True)
