# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChequeDeposit'
        db.create_table(u'bank_chequedeposit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_deposits', to=orm['ledger.Account'])),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('cheque_date', self.gf('django.db.models.fields.DateField')()),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
        ))
        db.send_create_signal(u'bank', ['ChequeDeposit'])


    def backwards(self, orm):
        # Deleting model 'ChequeDeposit'
        db.delete_table(u'bank_chequedeposit')


    models = {
        u'bank.chequedeposit': {
            'Meta': {'object_name': 'ChequeDeposit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cheque_deposits'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'cheque_date': ('django.db.models.fields.DateField', [], {}),
            'cheque_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'drawee_bank': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'drawee_bank_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ledger.account': {
            'Meta': {'object_name': 'Account'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ledger.category': {
            'Meta': {'object_name': 'Category'},
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
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['bank']