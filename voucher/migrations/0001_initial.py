# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Party'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Currency'])),
            ('tax', self.gf('django.db.models.fields.CharField')(default='inclusive', max_length=10)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
        ))
        db.send_create_signal(u'voucher', ['Invoice'])

        # Adding model 'InvoiceParticular'
        db.create_table('invoice_particular', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True, blank=True)),
            ('tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tax.TaxScheme'], null=True, blank=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='particulars', to=orm['voucher.Invoice'])),
        ))
        db.send_create_signal(u'voucher', ['InvoiceParticular'])

        # Adding model 'PurchaseVoucher'
        db.create_table(u'voucher_purchasevoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Party'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Currency'])),
            ('tax', self.gf('django.db.models.fields.CharField')(default='inclusive', max_length=10)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
        ))
        db.send_create_signal(u'voucher', ['PurchaseVoucher'])

        # Adding model 'PurchaseParticular'
        db.create_table('purchase_particular', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True, blank=True)),
            ('tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tax.TaxScheme'], null=True, blank=True)),
            ('purchase_voucher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='particulars', to=orm['voucher.PurchaseVoucher'])),
        ))
        db.send_create_signal(u'voucher', ['PurchaseParticular'])

        # Adding model 'JournalVoucher'
        db.create_table(u'voucher_journalvoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
        ))
        db.send_create_signal(u'voucher', ['JournalVoucher'])

        # Adding model 'JournalVoucherRow'
        db.create_table(u'voucher_journalvoucherrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('dr_account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='dr_rows', null=True, to=orm['ledger.Account'])),
            ('cr_account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cr_rows', null=True, to=orm['ledger.Account'])),
            ('dr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('journal_voucher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['voucher.JournalVoucher'])),
        ))
        db.send_create_signal(u'voucher', ['JournalVoucherRow'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('invoice')

        # Deleting model 'InvoiceParticular'
        db.delete_table('invoice_particular')

        # Deleting model 'PurchaseVoucher'
        db.delete_table(u'voucher_purchasevoucher')

        # Deleting model 'PurchaseParticular'
        db.delete_table('purchase_particular')

        # Deleting model 'JournalVoucher'
        db.delete_table(u'voucher_journalvoucher')

        # Deleting model 'JournalVoucherRow'
        db.delete_table(u'voucher_journalvoucherrow')


    models = {
        u'core.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'currency'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_usd_rate': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.category': {
            'Meta': {'object_name': 'Category'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_categories'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'inventory.inventoryaccount': {
            'Meta': {'object_name': 'InventoryAccount'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_balance': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'item'", 'unique': 'True', 'to': u"orm['inventory.InventoryAccount']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'Meta': {'unique_together': "(('company', 'name'), ('company', 'code'))", 'object_name': 'Account'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_cr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'opening_dr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ledger.category': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Category'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'ledger.party': {
            'Meta': {'object_name': 'Party', 'db_table': "'party'"},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'debtor_level': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'tax.taxscheme': {
            'Meta': {'object_name': 'TaxScheme'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'percent': ('django.db.models.fields.FloatField', [], {})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'voucher.invoice': {
            'Meta': {'object_name': 'Invoice', 'db_table': "'invoice'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Party']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.CharField', [], {'default': "'inclusive'", 'max_length': '10'})
        },
        u'voucher.invoiceparticular': {
            'Meta': {'object_name': 'InvoiceParticular', 'db_table': "'invoice_particular'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'particulars'", 'to': u"orm['voucher.Invoice']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tax.TaxScheme']", 'null': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.journalvoucher': {
            'Meta': {'object_name': 'JournalVoucher'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'voucher.journalvoucherrow': {
            'Meta': {'object_name': 'JournalVoucherRow'},
            'cr_account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cr_rows'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'cr_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dr_account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dr_rows'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'dr_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['voucher.JournalVoucher']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'voucher.purchaseparticular': {
            'Meta': {'object_name': 'PurchaseParticular', 'db_table': "'purchase_particular'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'purchase_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'particulars'", 'to': u"orm['voucher.PurchaseVoucher']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tax.TaxScheme']", 'null': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.purchasevoucher': {
            'Meta': {'object_name': 'PurchaseVoucher'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Party']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.CharField', [], {'default': "'inclusive'", 'max_length': '10'})
        }
    }

    complete_apps = ['voucher']