# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ChequeDeposit'
        db.delete_table(u'bank_chequedeposit')

        # Adding model 'ChequeDepositRow'
        db.create_table(u'bank_chequereceiptrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')()),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'bank', ['ChequeDepositRow'])

        # Adding model 'ChequeDeposit'
        db.create_table(u'bank_chequereceipt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_deposits', to=orm['ledger.Account'])),
            ('clearing_date', self.gf('django.db.models.fields.DateField')()),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('narration', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bank', ['ChequeDeposit'])


    def backwards(self, orm):
        # Adding model 'ChequeDeposit'
        db.create_table(u'bank_chequedeposit', (
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('cheque_date', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_deposits', to=orm['ledger.Account'])),
        ))
        db.send_create_signal(u'bank', ['ChequeDeposit'])

        # Deleting model 'ChequeDepositRow'
        db.delete_table(u'bank_chequereceiptrow')

        # Deleting model 'ChequeDeposit'
        db.delete_table(u'bank_chequereceipt')


    models = {
        u'bank.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'ac_no': ('django.db.models.fields.IntegerField', [], {}),
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ledger.Account']", 'unique': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'branch_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'bank.chequereceipt': {
            'Meta': {'object_name': 'ChequeDeposit'},
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cheque_deposits'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'clearing_date': ('django.db.models.fields.DateField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {})
        },
        u'bank.chequereceiptrow': {
            'Meta': {'object_name': 'ChequeDepositRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cheque_date': ('django.db.models.fields.DateField', [], {}),
            'cheque_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'drawee_bank': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'drawee_bank_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
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