# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VoucherSetting.company'
        db.add_column(u'core_vouchersetting', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VoucherSetting.company'
        db.delete_column(u'core_vouchersetting', 'company_id')


    models = {
        u'core.companysetting': {
            'Meta': {'object_name': 'CompanySetting'},
            'account_coding': ('django.db.models.fields.CharField', [], {'default': "'Automatic'", 'max_length': '9'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'decimal_places': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'default_currency': ('django.db.models.fields.related.ForeignKey', [], {'default': '144', 'to': u"orm['core.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_comma_system': ('django.db.models.fields.CharField', [], {'default': "'120,000'", 'max_length': '8'}),
            'region_setting': ('django.db.models.fields.CharField', [], {'default': "'North America'", 'max_length': '15'})
        },
        u'core.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'currency'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_usd_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.vouchersetting': {
            'Meta': {'object_name': 'VoucherSetting'},
            'bank_cash_deposit_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'bank_cash_deposit_heading': ('django.db.models.fields.CharField', [], {'default': "'Bank Cash Deposit'", 'max_length': '100'}),
            'bank_cash_deposit_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'bank_cash_deposit_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_payment_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'cash_payment_heading': ('django.db.models.fields.CharField', [], {'default': "'Cash Payment'", 'max_length': '100'}),
            'cash_payment_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_payment_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_receipt_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'cash_receipt_heading': ('django.db.models.fields.CharField', [], {'default': "'Cash Receipt'", 'max_length': '100'}),
            'cash_receipt_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_receipt_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_deposit_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'cheque_deposit_heading': ('django.db.models.fields.CharField', [], {'default': "'Cheque Deposit'", 'max_length': '100'}),
            'cheque_deposit_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_deposit_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_payment_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'cheque_payment_heading': ('django.db.models.fields.CharField', [], {'default': "'Cheque Payment'", 'max_length': '100'}),
            'cheque_payment_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_payment_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'eft_in_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'eft_in_heading': ('django.db.models.fields.CharField', [], {'default': "'EFT In'", 'max_length': '100'}),
            'eft_in_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'eft_in_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'eft_out_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'eft_out_heading': ('django.db.models.fields.CharField', [], {'default': "'EFT Out'", 'max_length': '100'}),
            'eft_out_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'eft_out_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'fixed_assets_purchase_voucher_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'fixed_assets_purchase_voucher_heading': ('django.db.models.fields.CharField', [], {'default': "'Fixed Assets Purchase Voucher'", 'max_length': '100'}),
            'fixed_assets_purchase_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'fixed_assets_purchase_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'invoice_heading': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'invoice_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'invoice_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal_voucher_heading': ('django.db.models.fields.CharField', [], {'default': "'Journal Voucher'", 'max_length': '100'}),
            'journal_voucher_purchase_voucher_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'journal_voucher_purchase_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal_voucher_purchase_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'purchase_voucher_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'purchase_voucher_heading': ('django.db.models.fields.CharField', [], {'default': "'Purchase Voucher'", 'max_length': '100'}),
            'purchase_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'purchase_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'voucher_number_restart_days': ('django.db.models.fields.IntegerField', [], {}),
            'voucher_number_restart_months': ('django.db.models.fields.IntegerField', [], {}),
            'voucher_number_restart_years': ('django.db.models.fields.IntegerField', [], {}),
            'voucher_number_start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['core']