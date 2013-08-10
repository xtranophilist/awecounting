from django.db import models
from users.models import Company
from ledger.models import Account


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=254)
    ac_no = models.IntegerField()
    branch_name = models.CharField(max_length=254, blank=True, null=True)
    account = models.ForeignKey(Account)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(code=self.ac_no, name=self.bank_name)
            account.save()
            self.account = account
        super(BankAccount, self).save(*args, **kwargs)


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True, blank=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    debtor_choices = [(1, 'Good'), (2, 'Bad'), (3, 'Ugly')]
    debtor_level = models.IntegerField(choices=debtor_choices, default=1, null=True, blank=True)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            account = Account(code=self.ac_no, name=self.bank_name)
            account.save()
            self.account = account
        super(Party, self).save(*args, **kwargs)

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
    invoice_prefix = models.CharField(max_length=5, default='INV-', blank=True, null=True)
    invoice_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    invoice_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in unique Invoice #')
    default_currency = models.ForeignKey(Currency)

    def __unicode__(self):
        return self.company.name


