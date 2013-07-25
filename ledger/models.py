from django.db import models


class Account(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return '/account/' + str(self.id)

    def __unicode__(self):
        return self.name
