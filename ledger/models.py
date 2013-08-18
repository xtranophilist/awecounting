from django.db import models
from users.models import Company
from core.models import Tag
from datetime import date


class Account(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    current_balance = models.FloatField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    tags = models.ManyToManyField(Tag, related_name='accounts', blank=True)

    def get_absolute_url(self):
        return '/account/' + str(self.id)

    def get_last_day_last_transaction(self):
        transactions = Transaction.objects.filter(account=self, date__lt=date.today()).order_by('-id', '-date')[:1]
        if len(transactions) > 0:
            return transactions[0]

    def get_last_transaction_before(self, before_date):
        transactions = Transaction.objects.filter(account=self, date__lt=before_date).order_by('-id', '-date')[:1]
        if len(transactions) > 0:
            return transactions[0]

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name='transactions')
    date = models.DateField()
    amount = models.FloatField()
    current_balance = models.FloatField()
    type = models.CharField(max_length=2)  # Dr. or Cr.


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
            account = Account(name=self.name)
            account.save()
            self.account = account
        super(Party, self).save(*args, **kwargs)

    class Meta:
        db_table = 'party'