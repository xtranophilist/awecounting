# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'inventory_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('purchase_price', self.gf('django.db.models.fields.FloatField')()),
            ('purchase_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_items',
                                                                                       to=orm['ledger.Account'])),
            ('purchase_tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_items',
                                                                                          to=orm['tax.TaxScheme'])),
            ('sales_price', self.gf('django.db.models.fields.FloatField')()),
            ('sales_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sales_items',
                                                                                    to=orm['ledger.Account'])),
            ('sales_tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sales_items',
                                                                                       to=orm['tax.TaxScheme'])),
        ))
        db.send_create_signal(u'inventory', ['Item'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'inventory_item')


    models = {
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
        }
    }

    complete_apps = ['inventory']