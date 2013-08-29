from django.db import models
from users.models import Company
from datetime import date
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'ledger_category'
        verbose_name_plural = u'Categories'


class Account(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    current_balance = models.FloatField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    category = models.ForeignKey(Category, related_name='accounts', blank=True)
    tax_rate = models.FloatField(blank=True, null=True)

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

    def get_day_opening(self, before_date=None):
        if not before_date:
            day = date.today()
        transactions = Transaction.objects.filter(account=self, date__lt=day).order_by('-id', '-date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_balance
        return self.current_balance

    day_opening = property(get_day_opening)

    def add_category(self, category):
        # all_categories = self.get_all_categories()
        category_instance, created = Category.objects.get_or_create(name=category, company=self.company)
        # self.categories.add(category_instance)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name='transactions')
    date = models.DateField()
    amount = models.FloatField()
    current_balance = models.FloatField()
    type = models.CharField(max_length=2)  # Dr. or Cr.

    # TODO change current balance on save
    def save(self, *args, **kwargs):
        self.amount = float(self.amount)
        print '1. amount is ' + str(self.amount)
        print '2. current balance is ' + str(self.account.current_balance)
        if self.type == 'Dr':
            self.account.current_balance += self.amount
        if self.type == 'Cr':
            self.account.current_balance -= self.amount
        self.account.save()
        self.current_balance = self.account.current_balance
        print '3. current balance is ' + str(self.account.current_balance)
        super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.type == 'Dr':
            self.account.current_balance -= self.amount
        if self.type == 'Cr':
            self.account.current_balance += self.amount
        self.account.save()
        super(Transaction, self).delete(*args, **kwargs)


    # def dr(self, account, amount, date):
    #     self.type == 'Dr'
    #     self.amount = float(amount)
    #     self.date = date
    #     self.account = account
    #     # self.account.current_balance += float(amount)
    #     # self.account.save()
    #     # self.current_balance = self.account.current_balance
    #     self.save()
    #
    #
    # def cr(self, account, amount, date):
    #     self.type == 'Cr'
    #     self.amount = float(amount)
    #     self.date = date
    #     self.account = account
    #     # self.account.current_balance -= float(amount)
    #     # self.account.save()
    #     # self.current_balance = self.account.current_balance
    #     self.save()


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
            account.company = self.company
            account.save()
            account.add_category('Party', self.company)
            self.account = account
        super(Party, self).save(*args, **kwargs)

    class Meta:
        db_table = 'party'