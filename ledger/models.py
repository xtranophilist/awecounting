from django.db import models
from users.models import Company


class Account(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)

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
