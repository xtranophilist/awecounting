from django import forms
from django.core.urlresolvers import reverse_lazy

from acubor.lib import KOModelForm, ExtFileField
from models import BankAccount, ChequeDeposit, BankCashDeposit, ChequePayment, ElectronicFundTransferIn, ElectronicFundTransferOut
from ledger.models import Account


class BankAccountForm(KOModelForm):
    class Meta:
        model = BankAccount
        exclude = ['company', 'account']


class ChequeDepositForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
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

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(ChequeDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=self.company,
                                                                      category__name='Bank Account')
        self.fields['benefactor'].queryset = Account.objects.filter(company=self.company)

    def clean_voucher_no(self):
        existing = ChequeDeposit.objects.filter(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
        import pdb
        pdb.set_trace()
        if existing.exists():
            raise forms.ValidationError("The voucher no. " + str(
                self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
        else:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = ChequeDeposit
        exclude = ['company', 'status']


class ElectronicFundTransferInForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
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

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ElectronicFundTransferInForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=company, category__name='Bank Account')
        self.fields['benefactor'].queryset = Account.objects.filter(company=company)

    class Meta:
        model = ElectronicFundTransferIn
        exclude = ['company']


class BankCashDepositForm(KOModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2', 'data-field': 'Bank Acc.',
                                                                     'data-add-url': reverse_lazy(
                                                                         'create_bank_account')}),
                                          label='Beneficiary Account')
    benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                        widget=forms.Select(
                                            attrs={'class': 'select2', 'data-add-url': reverse_lazy('create_account')}))
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(BankCashDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=company, category__name='Bank Account')
        self.fields['benefactor'].queryset = Account.objects.filter(company=company)

    class Meta:
        model = BankCashDeposit
        exclude = ['company']


class ChequePaymentForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
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

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ChequePaymentForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=company, category__name='Bank Account')
        self.fields['beneficiary'].queryset = Account.objects.filter(company=company)

    class Meta:
        model = ChequePayment
        exclude = ['company']


class ElectronicFundTransferOutForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
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

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ElectronicFundTransferOutForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=company, category__name='Bank Account')
        self.fields['beneficiary'].queryset = Account.objects.filter(company=company)

    class Meta:
        model = ElectronicFundTransferOut
        exclude = ['company']