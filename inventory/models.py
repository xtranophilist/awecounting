from django.db import models
from tax.models import TaxScheme
from ledger.models import Account
from users.models import Company
from datetime import date
from core.models import Tag

class Category(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '[' + self.code + '] ' + self.name


class Item(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    purchase_price = models.FloatField()
    purchase_account = models.ForeignKey(Account, related_name='purchase_items')
    purchase_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='purchase_items')
    sales_price = models.FloatField()
    sales_account = models.ForeignKey(Account, related_name='sales_items')
    sales_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='sales_items')
    company = models.ForeignKey(Company)
    category = models.ForeignKey(Category)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = InventoryAccount(code=self.ac_no, name=self.name)
            account.company = self.company
            account.save()
            # account.add_tag('Bank')
            self.account = account
        super(Item, self).save(*args, **kwargs)

    def add_tag(self, tag):
        # all_tags = self.get_all_tags()
        tag_instance, created = Tag.objects.get_or_create(name=tag)
        self.tags.add(tag_instance)

    def __unicode__(self):
        return '[' + self.code + '] ' + self.name


class InventoryAccount(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    item = models.ForeignKey(Item)

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    def get_last_day_last_transaction(self):
        transactions = InventoryTransaction.objects.filter(account=self, date__lt=date.today()).order_by('-id', '-date')[:1]
        if len(transactions) > 0:
            return transactions[0]

    def get_last_transaction_before(self, before_date):
        transactions = InventoryTransaction.objects.filter(account=self, date__lt=before_date).order_by('-id', '-date')[:1]
        if len(transactions) > 0:
            return transactions[0]

    def __unicode__(self):
        return self.name


class InventoryTransaction(models.Model):
    account = models.ForeignKey(InventoryAccount, related_name='transactions')
    date = models.DateField()
    quantity = models.FloatField()
    type = models.CharField(max_length=3)  # in or out
    current_quantity = models.FloatField()

