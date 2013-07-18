from django.db import models

class Item(models.Model):
    code = models.CharField(max_length=100)
