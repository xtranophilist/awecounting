from datetime import date
from datetime import timedelta

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import F
from mptt.models import MPTTModel, TreeForeignKey

from tax.models import TaxScheme
from ledger.models import Account
from users.models import Company
from acubor.lib import zero_for_none, none_for_zero


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    company = models.ForeignKey(Company, related_name='inventory_categories')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u' Inventory Categories'
        unique_together = (('company', 'name'),)


class InventoryAccount(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    opening_balance = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    def get_unit(self):
        try:
            item = self.item
        except:
            return None
        try:
            short_name = self.item.unit.short_name
        except:
            return None
        return short_name

    def get_category(self):
        try:
            item = self.item
        except:
            return None
        try:
            category = self.item.category
        except:
            return None
        return category

    # def get_day_opening_dr(self, before_date=None):
    #     if not before_date:
    #         before_date = date.today()
    #     transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
    #         '-journal_entry__id', '-journal_entry__date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0].current_dr
    #     return self.current_dr
    #
    # def get_day_opening_cr(self, before_date=None):
    #     if not before_date:
    #         before_date = date.today()
    #     transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
    #         '-journal_entry__id', '-journal_entry__date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0].current_cr
    #     return self.current_cr

    def get_day_opening(self, before_date=None):
        if not before_date:
            before_date = date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return zero_for_none(transactions[0].current_dr) - zero_for_none(transactions[0].current_dr)
        return self.opening_balance

    # day_opening_dr = property(get_day_opening_dr)
    # day_opening_cr = property(get_day_opening_cr)
    #
    # day_opening = property(get_day_opening)

    def add_category(self, category):
        # all_categories = self.get_all_categories()
        category_instance, created = Category.objects.get_or_create(name=category, company=self.company)
        # self.categories.add(category_instance)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    def get_cr_amount(self, day):
        #journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return 0

    def get_dr_amount(self, day):
        #journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return 0


class Unit(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)
    company = models.ForeignKey(Company)

    def __str__(self):
        return self.name


class Item(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    purchase_price = models.FloatField(blank=True, null=True)
    purchase_account = models.ForeignKey(Account, related_name='purchase_items')
    purchase_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='purchase_items')
    sales_price = models.FloatField(blank=True, null=True)
    sales_account = models.ForeignKey(Account, related_name='sales_items')
    sales_tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', related_name='sales_items')
    company = models.ForeignKey(Company)
    category = models.ForeignKey(Category, null=True, blank=True)
    account = models.OneToOneField(InventoryAccount, related_name='item')
    opening_stock = models.FloatField(default=0)
    unit = models.ForeignKey(Unit, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = InventoryAccount(code=self.code, name=self.name, opening_balance=self.opening_stock)
            account.company = self.company
            account.save()
            # account.add_category('Bank')
            self.account = account
        super(Item, self).save(*args, **kwargs)

    def add_category(self, category):
        # all_categories = self.get_all_categories()
        category_instance, created = Category.objects.get_or_create(name=category)
        self.categories.add(category_instance)

    def __unicode__(self):
        return '[' + self.code + '] ' + self.name


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType, related_name='inventory_journal_entries')
    model_id = models.IntegerField()

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.model_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'InventoryJournal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(InventoryAccount)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


def alter(account, date, dr_difference, cr_difference):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))


def set_transactions(submodel, date, *args):
    # [transaction.delete() for transaction in submodel.transactions.all()]
    # args = [arg for arg in args if arg is not None]
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), model_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
                transaction.account.current_dr = none_for_zero(
                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
                alter(arg[1], date, float(arg[2]), 0)
            if arg[0] == 'cr':
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None
                transaction.account.current_cr = none_for_zero(
                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
                alter(arg[1], date, 0, float(arg[2]))
            transaction.current_dr = none_for_zero(
                zero_for_none(transaction.account.get_dr_amount(date + timedelta(days=1)))
                + zero_for_none(transaction.dr_amount))
            transaction.current_cr = none_for_zero(
                zero_for_none(transaction.account.get_cr_amount(date + timedelta(days=1)))
                + zero_for_none(transaction.cr_amount))
        else:
            transaction = matches[0]
            transaction.account = arg[1]

            # cancel out existing dr_amount and cr_amount from current_dr and current_cr
            # if transaction.dr_amount:
            #     transaction.current_dr -= transaction.dr_amount
            #     transaction.account.current_dr -= transaction.dr_amount
            #
            # if transaction.cr_amount:
            #     transaction.current_cr -= transaction.cr_amount
            #     transaction.account.current_cr -= transaction.cr_amount

            # save new dr_amount and add it to current_dr/cr
            if arg[0] == 'dr':
                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
            else:
                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None

            transaction.current_dr = none_for_zero(zero_for_none(transaction.current_dr) + dr_difference)
            transaction.current_cr = none_for_zero(zero_for_none(transaction.current_cr) + cr_difference)
            transaction.account.current_dr = none_for_zero(
                zero_for_none(transaction.account.current_dr) + dr_difference)
            transaction.account.current_cr = none_for_zero(
                zero_for_none(transaction.account.current_cr) + cr_difference)

        #the following code lies outside if,else block, inside for loop
        transaction.account.save()
        journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                     model_id=instance.id).delete()
            instance.delete()


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    print transaction
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr -= transaction.cr_amount

    print transaction.dr_amount
    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()