from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, identifier=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=UserManager.normalize_email(email),
            full_name=full_name,
            identifier=identifier,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        """
        Creates and saves a superuser with the given email, full name and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Company(models.Model):
    name = models.CharField(max_length=254)
    location = models.TextField()
    type_of_business = models.CharField(max_length=254)

    class Meta:
        db_table = u'company'


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=245)
    email = models.EmailField(verbose_name='email address', max_length=254, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    identifier = models.CharField(max_length=245, null=True)
    company = models.ForeignKey(Company, null=True)

    # USERNAME_FIELD = 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def __unicode__(self):
        return self.username

    objects = UserManager()

    class Meta:
        db_table = u'user'
