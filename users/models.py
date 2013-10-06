from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from acubor import settings


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, full_name='', identifier=None):
        # import pdb
        # pdb.set_trace()
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            full_name=full_name,
            identifier=identifier,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, full_name=''):
        """
        Creates and saves a superuser with the given email, full name and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Company(models.Model):
    name = models.CharField(max_length=254)
    location = models.TextField()
    type_of_business = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'company'
        verbose_name_plural = u'Companies'


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=245)
    email = models.EmailField(verbose_name='email address', max_length=254, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    identifier = models.CharField(max_length=245, null=True)
    #company = models.ForeignKey(Company, null=True)
    #groups = models.ManyToManyField(Group, related_name='users')

    # USERNAME_FIELD = 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        # The user is identified by username
        return self.username

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email):
        pass

    def get_company_settings(self):
        from core.models import CompanySetting

        return CompanySetting.objects.get(company=self.company)

    objects = UserManager()

    class Meta:
        db_table = u'user'


def create_default(company):
    from ledger.models import Account, Category

    equity = Category(name='Equity', company=company)
    equity.save()
    Account(name='Paid in Capital', category=equity, code='1-0001', company=company).save()
    Account(name='Retained Earnings', category=equity, code='1-0002', company=company).save()
    Account(name='Profit and Loss Account', category=equity, code='1-0003', company=company).save()

    assets = Category(name='Assets', company=company)
    assets.save()
    bank_account = Category(name='Bank Account', parent=assets, company=company)
    bank_account.save()
    Account(name='Bank Account', category=bank_account, code='2-0001', company=company).save()
    Account(name='Card Account', category=bank_account, code='2-0002', company=company).save()

    cash_account = Category(name='Cash Account', parent=assets, company=company)
    cash_account.save()
    Account(name='Cash Account', category=cash_account, code='2-0004', company=company).save()
    Account(name='ATM Account', category=bank_account, code='2-0005', company=company).save()
    cash_equivalent_account = Category(name='Cash Equivalent Account', parent=assets, company=company)
    cash_equivalent_account.save()
    Account(name='Cheque Account', category=cash_equivalent_account, code='2-0003', company=company).save()
    Account(name='Food Stamps Account', category=cash_equivalent_account, code='2-0006', company=company).save()
    Account(name='Coupons Account', category=cash_equivalent_account, code='2-0007', company=company).save()
    Account(name='Merchandise', category=assets, code='2-0008', company=company).save()
    Category(name='Account Receivables', parent=assets, company=company).save()
    Category(name='Other Receivables', parent=assets, company=company).save()
    Category(name='Deferred Assets', parent=assets, company=company).save()
    Category(name='Fixed Assets', parent=assets, company=company).save()
    Category(name='Loads and Advances Given', parent=assets, company=company).save()
    Category(name='Deposits Made', parent=assets, company=company).save()

    liabilities = Category(name='Liabilities', company=company)
    liabilities.save()
    Category(name='Account Payables', parent=liabilities, company=company).save()
    other_payables = Category(name='Other Payables', parent=liabilities, company=company)
    other_payables.save()
    Account(name='Utility Bills Account', category=other_payables, code='3-0002', company=company).save()
    Category(name='Provisions', parent=liabilities, company=company).save()
    secured_loans = Category(name='Secured Loans', parent=liabilities, company=company)
    secured_loans.save()
    Account(name='Bank OD', category=secured_loans, code='3-0005', company=company).save()
    Account(name='Bank Loans', category=secured_loans, code='3-0006', company=company).save()
    Category(name='Unsecured Loans', parent=liabilities, company=company).save()
    Category(name='Deposits Taken', parent=liabilities, company=company).save()
    Category(name='Loans & Advances Taken', parent=liabilities, company=company).save()
    duties_and_taxes = Category(name='Duties & Taxes', parent=liabilities, company=company)
    duties_and_taxes.save()
    Account(name='Sales Tax', category=duties_and_taxes, code='3-0010', company=company).save()
    Account(name='Payroll Tax', category=duties_and_taxes, code='3-0011', company=company).save()
    Account(name='Income Tax', category=duties_and_taxes, code='3-0012', company=company).save()

    income = Category(name='Income', company=company)
    income.save()
    sales = Category(name='Sales', parent=income, company=company)
    sales.save()
    Account(name='Fuel Sales', category=sales, code='4-0001', company=company).save()
    Account(name='Cigarette/Tobacco Sales', category=sales, code='4-0002', company=company).save()
    Account(name='Soda Sales', category=sales, code='4-0003', company=company).save()
    Account(name='Water Sales', category=sales, code='4-0004', company=company).save()
    Account(name='Newspaper Sales', category=sales, code='4-0005', company=company).save()
    Account(name='Non Tax Sales', category=sales, code='4-0006', company=company).save()
    Account(name='Telephone PP Card Sales', category=sales, code='4-0007', company=company).save()
    Account(name='Sales', category=sales, code='4-0008', company=company).save()
    Account(name='Scratch Off Sales', category=sales, code='4-0009', company=company).save()
    Account(name='Lotto Sales', category=sales, code='4-0010', company=company).save()
    Account(name='Moneygram Sales', category=sales, code='4-0011', company=company).save()
    Category(name='Direct Income', parent=income, company=company).save()
    indirect_income = Category(name='Indirect Income', parent=income, company=company)
    indirect_income.save()
    Account(name='Commission In', category=indirect_income, code='6-0001', company=company).save()

    expenses = Category(name='Expenses', company=company)
    expenses.save()
    purchase = Category(name='Purchase', parent=expenses, company=company)
    purchase.save()
    Account(name='Fuel Purchase', category=purchase, code='11-0001', company=company).save()
    Account(name='Cigarette/Tobacco Purchase', category=purchase, code='11-0002', company=company).save()
    Account(name='Soda Purchase', category=purchase, code='11-0003', company=company).save()
    Account(name='Water Purchase', category=purchase, code='11-0004', company=company).save()
    Account(name='Newspaper Purchase', category=purchase, code='11-0005', company=company).save()
    Account(name='Non Tax Purchase', category=purchase, code='11-0006', company=company).save()
    Account(name='Telephone PP Card Purchase', category=purchase, code='11-0007', company=company).save()
    Account(name='Purchase', category=purchase, code='11-0008', company=company).save()
    Account(name='Scratch Off Purchase', category=purchase, code='11-0009', company=company).save()
    Account(name='Lotto Purchase', category=purchase, code='11-0010', company=company).save()
    Account(name='Moneygram Purchase', category=purchase, code='11-0011', company=company).save()

    Category(name='Direct Expenses', parent=expenses, company=company).save()

    indirect_expenses = Category(name='Indirect Expenses', parent=expenses, company=company)
    indirect_expenses.save()
    Account(name='Payroll Expenses', category=indirect_expenses, code='13-0001', company=company).save()
    Account(name='Rent Expenses', category=indirect_expenses, code='13-0002', company=company).save()
    Account(name='Commission Out', category=indirect_expenses, code='13-0003', company=company).save()
    Account(name='Bank Charges Expenses', category=indirect_expenses, code='13-0004', company=company).save()
    Account(name='Bank Interest Expenses', category=indirect_expenses, code='13-0005', company=company).save()
    Account(name='Electricity Expenses', category=indirect_expenses, code='13-0006', company=company).save()
    Account(name='City/Municipal Expenses', category=indirect_expenses, code='13-0007', company=company).save()
    Account(name='Travelling and Conveyance Expenses', category=indirect_expenses, code='13-0008',
            company=company).save()
    Account(name='Lunch and Refreshment Expenses', category=indirect_expenses, code='13-0009', company=company).save()
    Account(name='Cleaning Expenses', category=indirect_expenses, code='13-0010', company=company).save()
    Account(name='Discounting Expenses', category=indirect_expenses, code='13-0011', company=company).save()
    Account(name='Repairs and Maintenance Expenses', category=indirect_expenses, code='13-0012', company=company).save()

    opening_balance_difference = Category(name='Opening Balance Difference', company=company)
    opening_balance_difference.save()
    Account(name='Opening Balance Difference', category=opening_balance_difference, company=company,
            code='0-0001').save()


class Role(models.Model):
    user = models.ForeignKey(User, related_name='roles')
    group = models.ForeignKey(Group, related_name='roles')
    company = models.ForeignKey(Company, related_name='roles')

    def __str__(self):
        return self.group.name

    class Meta:
        unique_together = ('user', 'group', 'company')


def handle_new_user(sender, user, request, **kwargs):
    user.full_name = request.POST.get('full_name')
    company = Company()
    company.name = request.POST.get('name_of_company')
    company.location = request.POST.get('location')
    company.type_of_business = request.POST.get('type_of_business')
    company.save()
    user.company = company
    user.is_active = True
    user.save()
    try:
        role = Role(user=user, group=Group.objects.get(name='SuperOwner'), company=company)
        role.save()
    except Group.DoesNotExist:
        pass
    create_default(company)


from registration.signals import user_registered

user_registered.connect(handle_new_user)


def group_required(*groups):
    def _dec(view_function):

        def _view(request, *args, **kwargs):
            allowed = False
            for role in request.roles:
                if role.group.name in groups:
                    allowed = True
            if allowed:
                return view_function(request, *args, **kwargs)
            else:
                if request.user.is_authenticated():
                    return HttpResponseForbidden("You don't have permission to view this page!")
                else:
                    return redirect(settings.LOGIN_URL)


        return _view

    return _dec

