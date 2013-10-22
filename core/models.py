from django.db import models
from users.models import Company


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    latest_usd_rate = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Currencies'
        db_table = 'currency'

    def __unicode__(self):
        return self.code + ' - ' + self.name


class CompanySetting(models.Model):
    company = models.ForeignKey(Company)
    default_currency = models.ForeignKey(Currency, default=144)
    decimal_places = models.IntegerField(default=2)
    number_comma_system = models.CharField(choices=[('1,20,000', '1,20,000'), ('120,000', '120,000')], max_length=8,
                                           default='120,000')
    region_setting = models.CharField(
        choices=[('North America', 'North America'), ('South America', 'South America'), ('Europe', 'Europe'),
                 ('Africa', 'Africa'), ('Asia/Pacific', 'Asia/Pacific')], max_length=15, default='North America')
    account_coding = models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=9,
                                      default='Automatic')
    #default_dayjournal = models.ForeignKey(DayJournal, null=True, blank=True)

    def __unicode__(self):
        return self.company.name


class VoucherSetting(models.Model):
    voucher_number_start_date = models.DateField()
    voucher_number_restart_years = models.IntegerField()
    voucher_number_restart_months = models.IntegerField()
    voucher_number_restart_days = models.IntegerField()

    invoice_heading = models.CharField(max_length=100)
    invoice_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    invoice_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    invoice_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in unique Invoice #')

    purchase_voucher_heading = models.CharField(default='Purchase Voucher', max_length=100)
    purchase_voucher_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    purchase_voucher_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    purchase_voucher_digit_count = models.IntegerField(default=4,
                                                       verbose_name='Number of digits in unique Purchase Voucher#')

    fixed_assets_purchase_voucher_heading = models.CharField(default='Fixed Assets Purchase Voucher', max_length=100)
    fixed_assets_purchase_voucher_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    fixed_assets_purchase_voucher_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    fixed_assets_purchase_voucher_digit_count = models.IntegerField(default=4,
                                                                    verbose_name='Number of digits in Fixed Assets Purchase Voucher#')

    journal_voucher_heading = models.CharField(default='Journal Voucher', max_length=100)
    journal_voucher_purchase_voucher_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    journal_voucher_purchase_voucher_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    journal_voucher_purchase_voucher_digit_count = models.IntegerField(default=4,
                                                                       verbose_name='Number of digits in Journal Voucher#')

    cash_receipt_heading = models.CharField(default='Cash Receipt', max_length=100)
    cash_receipt_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    cash_receipt_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    cash_receipt_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in Cash Receipt#')

    cash_payment_heading = models.CharField(default='Cash Payment', max_length=100)
    cash_payment_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    cash_payment_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    cash_payment_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in Cash Payment#')

    bank_cash_deposit_heading = models.CharField(default='Bank Cash Deposit', max_length=100)
    bank_cash_deposit_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    bank_cash_deposit_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    bank_cash_deposit_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in Cash Deposit#')

    cheque_deposit_heading = models.CharField(default='Cheque Deposit', max_length=100)
    cheque_deposit_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    cheque_deposit_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    cheque_deposit_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in Cheque Deposit#')

    cheque_payment_heading = models.CharField(default='Cheque Payment', max_length=100)
    cheque_payment_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    cheque_payment_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    cheque_payment_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in Cheque Payment#')

    eft_in_heading = models.CharField(default='EFT In', max_length=100)
    eft_in_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    eft_in_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    eft_in_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in EFT In#')

    eft_out_heading = models.CharField(default='EFT Out', max_length=100)
    eft_out_prefix = models.CharField(max_length=5, default='', blank=True, null=True)
    eft_out_suffix = models.CharField(max_length=5, default='', blank=True, null=True)
    eft_out_digit_count = models.IntegerField(default=4, verbose_name='Number of digits in EFT Out#')