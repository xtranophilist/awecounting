from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(verbose_name='email address', max_length=254, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin