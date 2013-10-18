import datetime

from django.db import models

from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=254)
    author = models.ForeignKey(User)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    content = models.TextField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        timestamp = datetime.datetime.today()
        if not self.id:
            self.created = timestamp
        self.updated = timestamp
        return super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
