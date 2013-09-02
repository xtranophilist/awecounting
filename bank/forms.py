from acubor.lib import KOModelForm, ExtFileField
from django import forms
from models import BankAccount, ChequeDeposit, BankCashDeposit, ChequePayment
from ledger.models import Account


class BankAccountForm(KOModelForm):
    class Meta:
        model = BankAccount
        exclude = ['company', 'account']


class ChequeDepositForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2'}), label='Beneficiary Account')
    benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                        widget=forms.Select(attrs={'class': 'select2'}), label='Benefactor (Given By)')
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
    clearing_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}), required=False)
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    class Meta:
        model = ChequeDeposit
        exclude = ['company']


class BankCashDepositForm(KOModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2'}), label='Beneficiary Account')
    benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                        widget=forms.Select(attrs={'class': 'select2'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    class Meta:
        model = BankCashDeposit
        exclude = ['company']


class ChequePaymentForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2'}))
    beneficiary = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                        widget=forms.Select(attrs={'class': 'select2'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    class Meta:
        model = ChequePayment
        exclude = ['company']