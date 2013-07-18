from django.db import models

# Create your models here.

class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField(max_lenght=254)
    fax = models.CharField(max_length=20)

class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    latest_usd_rate = models.FloatField()



class Particular(models.Model):
    pass

class SalesVoucher(models.Model):
    party = models.ForeignKey(Party)
    date = models.DateField()
    due_date = models.DateField(null=True)
    invoice_no = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, null=True)
    currency = models.ForeignKey(Currency)
    tax = models.CharField(max_length=10)






