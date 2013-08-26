from django.db import models
from ledger.models import Account


class ChequeDeposit(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='cheque_deposits')
    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    drawee_bank = models.CharField(max_length=254, blank=True, null=True)
    drawee_bank_address = models.CharField(max_length=254, blank=True, null=True)
    amount = models.FloatField()
    cheque_date = models.DateField()
    benefactor = models.ForeignKey(Account)