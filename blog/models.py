from django.db import models
from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=254)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title
