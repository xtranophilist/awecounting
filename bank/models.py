from django.db import models
from ledger.models import Account
from users.models import Company


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=254)
    ac_no = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=254, blank=True, null=True)
    account = models.OneToOneField(Account)
    company = models.ForeignKey(Company)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(code=self.ac_no[-10:], name=self.bank_name + ' Account (' + str(self.ac_no) + ' )')
            account.company = self.company
            # account
            account.add_category('Bank Account')
            account.save()
            self.account = account
        super(BankAccount, self).save(*args, **kwargs)

    def __str__(self):
        return self.bank_name + ' Account (' + str(self.ac_no) + ' )'


class ChequeDeposit(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='cheque_deposits')
    clearing_date = models.DateField(null=True, blank=True)
    benefactor = models.ForeignKey(Account)
    attachment = models.FileField(upload_to='cheque_deposits/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/bank/cheque-deposit/' + str(self.id)


class ChequeDepositRow(models.Model):
    sn = models.IntegerField()
    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    drawee_bank = models.CharField(max_length=254, blank=True, null=True)
    drawee_bank_address = models.CharField(max_length=254, blank=True, null=True)
    amount = models.FloatField()
    cheque_deposit = models.ForeignKey(ChequeDeposit, related_name='rows')

    def get_absolute_url(self):
        return self.cheque_deposit.get_absolute_url()

    def get_voucher_number(self):
        return self.cheque_deposit.id


class BankCashDeposit(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='cash_deposits')
    benefactor = models.ForeignKey(Account)
    amount = models.FloatField()
    attachment = models.FileField(upload_to='bank_cash_deposits/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/bank/cash-deposit/' + str(self.id)


class ChequePayment(models.Model):
    cheque_number = models.CharField(max_length=50)
    date = models.DateField()
    beneficiary = models.ForeignKey(Account)
    bank_account = models.ForeignKey(Account, related_name='cheque_payments')
    amount = models.FloatField()
    attachment = models.FileField(upload_to='cheque_payments/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/bank/cheque-payment/' + str(self.id)


class ElectronicFundTransferOut(models.Model):
    transaction_number = models.CharField(max_length=50)
    date = models.DateField()
    beneficiary = models.ForeignKey(Account)
    bank_account = models.ForeignKey(Account, related_name='electronic_fund_transfer_out')
    amount = models.FloatField()
    attachment = models.FileField(upload_to='electronic_fund_transfer_out/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/bank/electronic-fund-transfer-out/' + str(self.id)


class ElectronicFundTransferIn(models.Model):
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='electronic_fund_transfer_in')
    clearing_date = models.DateField(null=True, blank=True)
    benefactor = models.ForeignKey(Account)
    attachment = models.FileField(upload_to='electronic_fund_transfer_in/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return '/bank/electronic-fund-transfer-in/' + str(self.id)


class ElectronicFundTransferInRow(models.Model):
    sn = models.IntegerField()
    transaction_number = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateField(blank=True, null=True)
    drawee_bank = models.CharField(max_length=254, blank=True, null=True)
    drawee_bank_address = models.CharField(max_length=254, blank=True, null=True)
    amount = models.FloatField()
    electronic_fund_transfer_in = models.ForeignKey(ElectronicFundTransferIn, related_name='rows')

    def get_absolute_url(self):
        return self.electronic_fund_transfer_in.get_absolute_url()

    def get_voucher_number(self):
        return self.electronic_fund_transfer_in.id


