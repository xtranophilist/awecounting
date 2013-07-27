from django.db import models
from users.models import Company


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    fax = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'party'


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    latest_usd_rate = models.FloatField()

    class Meta:
        verbose_name_plural = u'Currencies'
        db_table = 'currency'

    def __unicode__(self):
        return self.code + ' - ' + self.name


class CompanySetting(models.Model):
    company = models.ForeignKey(Company)
    invoice_prefix = models.CharField(max_length=5, default='INV-')
    invoice_suffix = models.CharField(max_length=5, default='')
    invoice_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in unique Invoice #')
    default_currency = models.ForeignKey(Currency)

    def __unicode__(self):
        return self.company.name



