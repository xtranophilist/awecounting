# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table(u'voucher_currency')

        # Deleting model 'Party'
        db.delete_table(u'voucher_party')


        # Changing field 'PurchaseVoucher.currency'
        db.alter_column(u'voucher_purchasevoucher', 'currency_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Currency']))

        # Changing field 'PurchaseVoucher.party'
        db.alter_column(u'voucher_purchasevoucher', 'party_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Party']))

        # Changing field 'SalesVoucher.currency'
        db.alter_column(u'voucher_salesvoucher', 'currency_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Currency']))

        # Changing field 'SalesVoucher.party'
        db.alter_column(u'voucher_salesvoucher', 'party_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Party']))

    def backwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'voucher_currency', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latest_usd_rate', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'voucher', ['Currency'])

        # Adding model 'Party'
        db.create_table(u'voucher_party', (
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'voucher', ['Party'])


        # Changing field 'PurchaseVoucher.currency'
        db.alter_column(u'voucher_purchasevoucher', 'currency_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Currency']))

        # Changing field 'PurchaseVoucher.party'
        db.alter_column(u'voucher_purchasevoucher', 'party_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Party']))

        # Changing field 'SalesVoucher.currency'
        db.alter_column(u'voucher_salesvoucher', 'currency_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Currency']))

        # Changing field 'SalesVoucher.party'
        db.alter_column(u'voucher_salesvoucher', 'party_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voucher.Party']))

    models = {
        u'core.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'currency'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_usd_rate': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.party': {
            'Meta': {'object_name': 'Party', 'db_table': "'party'"},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'purchase_account': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'purchase_items'", 'to': u"orm['ledger.Account']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'purchase_tax_scheme': ('django.db.models.fields.related.ForeignKey', [],
                                    {'related_name': "'purchase_items'", 'to': u"orm['tax.TaxScheme']"}),
            'sales_account': ('django.db.models.fields.related.ForeignKey', [],
                              {'related_name': "'sales_items'", 'to': u"orm['ledger.Account']"}),
            'sales_price': ('django.db.models.fields.FloatField', [], {}),
            'sales_tax_scheme': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'sales_items'", 'to': u"orm['tax.TaxScheme']"})
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
        u'voucher.particular': {
            'Meta': {'object_name': 'Particular'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'sales_voucher': ('django.db.models.fields.related.ForeignKey', [],
                              {'related_name': "'particulars'", 'to': u"orm['voucher.SalesVoucher']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tax.TaxScheme']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.purchasevoucher': {
            'Meta': {'object_name': 'PurchaseVoucher'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Party']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tax': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'voucher.salesvoucher': {
            'Meta': {'object_name': 'SalesVoucher'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Party']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tax': ('django.db.models.fields.CharField', [], {'default': "'inclusive'", 'max_length': '10'})
        }
    }

    complete_apps = ['voucher']