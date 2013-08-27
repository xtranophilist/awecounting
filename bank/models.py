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
            account = Account(code=self.ac_no, name=self.bank_name + ' Account (' + str(self.ac_no) + ' )')
            account.company = self.company
            # account
            account.add_category('Bank')
            account.save()
            self.account = account
        super(BankAccount, self).save(*args, **kwargs)


class ChequeReceipt(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='cheque_deposits')
    clearing_date = models.DateField(null=True, blank=True)
    benefactor = models.ForeignKey(Account)
    attachment = models.FileField(upload_to='cheque_receipts/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)


class ChequeReceiptRow(models.Model):
    sn = models.IntegerField()
    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    drawee_bank = models.CharField(max_length=254, blank=True, null=True)
    drawee_bank_address = models.CharField(max_length=254, blank=True, null=True)
    amount = models.FloatField()
    cheque_receipt = models.ForeignKey(ChequeReceipt, related_name='rows')


class BankCashReceipt(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='cash_deposits')
    benefactor = models.ForeignKey(Account)
    amount = models.FloatField()
    attachment = models.FileField(upload_to='bank_cash_receipts/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)


class ChequePayment(models.Model):
    cheque_number = models.CharField(max_length=50)
    date = models.DateField()
    beneficiary = models.ForeignKey(Account)
    bank_account = models.ForeignKey(Account, related_name='cheque_payments')
    amount = models.FloatField()
    attachment = models.FileField(upload_to='cheque_payments/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)