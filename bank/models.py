from django.db import models
from ledger.models import Account
from users.models import Company


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=254)
    ac_no = models.IntegerField()
    branch_name = models.CharField(max_length=254, blank=True, null=True)
    account = models.OneToOneField(Account)
    company = models.ForeignKey(Company)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(code=self.ac_no, name=self.bank_name)
            account.company = self.company
            # account
            account.add_category('Bank')
            account.save()
            self.account = account
        super(BankAccount, self).save(*args, **kwargs)


class ChequeReceipt(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='cheque_deposits')
    clearing_date = models.DateField()
    benefactor = models.ForeignKey(Account)
    narration = models.TextField()


class ChequeReceiptRow(models.Model):
    sn = models.IntegerField()
    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    cheque_date = models.DateField()
    drawee_bank = models.CharField(max_length=254, blank=True, null=True)
    drawee_bank_address = models.CharField(max_length=254, blank=True, null=True)
    amount = models.FloatField()
    cheque_receipt = models.ForeignKey(ChequeReceipt)
