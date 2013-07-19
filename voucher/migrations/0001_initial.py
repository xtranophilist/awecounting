# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Party'
        db.create_table(u'voucher_party', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'voucher', ['Party'])

        # Adding model 'Currency'
        db.create_table(u'voucher_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latest_usd_rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'voucher', ['Currency'])

        # Adding model 'Particular'
        db.create_table(u'voucher_particular', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.FloatField')()),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tax.TaxScheme'])),
        ))
        db.send_create_signal(u'voucher', ['Particular'])

        # Adding model 'SalesVoucher'
        db.create_table(u'voucher_salesvoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Party'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Currency'])),
            ('tax', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['SalesVoucher'])

        # Adding model 'PurchaseVoucher'
        db.create_table(u'voucher_purchasevoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Party'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Currency'])),
            ('tax', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['PurchaseVoucher'])


    def backwards(self, orm):
        # Deleting model 'Party'
        db.delete_table(u'voucher_party')

        # Deleting model 'Currency'
        db.delete_table(u'voucher_currency')

        # Deleting model 'Particular'
        db.delete_table(u'voucher_particular')

        # Deleting model 'SalesVoucher'
        db.delete_table(u'voucher_salesvoucher')

        # Deleting model 'PurchaseVoucher'
        db.delete_table(u'voucher_purchasevoucher')


    models = {
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'purchase_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_items'", 'to': u"orm['ledger.Account']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'purchase_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_items'", 'to': u"orm['tax.TaxScheme']"}),
            'sales_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_items'", 'to': u"orm['ledger.Account']"}),
            'sales_price': ('django.db.models.fields.FloatField', [], {}),
            'sales_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_items'", 'to': u"orm['tax.TaxScheme']"})
        },
        u'ledger.account': {
            'Meta': {'object_name': 'Account'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tax.taxscheme': {
            'Meta': {'object_name': 'TaxScheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'percent': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_usd_rate': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'voucher.particular': {
            'Meta': {'object_name': 'Particular'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tax.TaxScheme']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.party': {
            'Meta': {'object_name': 'Party'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'voucher.purchasevoucher': {
            'Meta': {'object_name': 'PurchaseVoucher'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voucher.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voucher.Party']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tax': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'voucher.salesvoucher': {
            'Meta': {'object_name': 'SalesVoucher'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voucher.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voucher.Party']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tax': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['voucher']