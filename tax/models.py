from django.db import models

class TaxScheme(models.Model):
    name = models.CharField(max_length=100)
    percent = models.FloatField()
