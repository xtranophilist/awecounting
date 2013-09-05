from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.models import PermissionsMixin


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
    company = models.ForeignKey(Company, null=True)

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


def handle_new_user(sender, user, request, **kwargs):
    user.full_name = request.POST.get('full_name')
    company = Company()
    company.name = request.POST.get('name_of_company')
    company.location = request.POST.get('location')
    company.type_of_business = request.POST.get('type_of_business')
    company.save()
    user.company = company
    # TODO: Add to group 'Owner'
    # import pdb
    # pdb.set_trace()
    # ownr, created = Group.objects.get_or_create(name='Owner')
    # ownr.user_set.add(user)
    # ownr.save()
    user.save()


from registration.signals import user_registered

user_registered.connect(handle_new_user)

