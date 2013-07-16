from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class User(AbstractBaseUser):
    full_name = models.CharField(max_length=245)
    email = models.EmailField(verbose_name='email address', max_length=254, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # USERNAME_FIELD = 'username'
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __unicode__(self):
        return self.username
