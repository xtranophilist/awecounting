# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntryRow'
        db.create_table(u'payroll_entryrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('pay_heading', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('hours', self.gf('django.db.models.fields.FloatField')()),
            ('tax', self.gf('django.db.models.fields.FloatField')()),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payroll.Entry'])),
        ))
        db.send_create_signal(u'payroll', ['EntryRow'])

        # Deleting field 'Entry.tax'
        db.delete_column(u'payroll_entry', 'tax')

        # Deleting field 'Entry.hours'
        db.delete_column(u'payroll_entry', 'hours')

        # Deleting field 'Entry.remarks'
        db.delete_column(u'payroll_entry', 'remarks')

        # Deleting field 'Entry.pay_heading'
        db.delete_column(u'payroll_entry', 'pay_heading')

        # Deleting field 'Entry.amount'
        db.delete_column(u'payroll_entry', 'amount')

        # Deleting field 'Entry.sn'
        db.delete_column(u'payroll_entry', 'sn')

        # Deleting field 'Entry.employee'
        db.delete_column(u'payroll_entry', 'employee_id')


    def backwards(self, orm):
        # Deleting model 'EntryRow'
        db.delete_table(u'payroll_entryrow')

        # Adding field 'Entry.tax'
        db.add_column(u'payroll_entry', 'tax',
                      self.gf('django.db.models.fields.FloatField')(default=None),
                      keep_default=False)

        # Adding field 'Entry.hours'
        db.add_column(u'payroll_entry', 'hours',
                      self.gf('django.db.models.fields.FloatField')(default=None),
                      keep_default=False)

        # Adding field 'Entry.remarks'
        db.add_column(u'payroll_entry', 'remarks',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.pay_heading'
        db.add_column(u'payroll_entry', 'pay_heading',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=254),
                      keep_default=False)

        # Adding field 'Entry.amount'
        db.add_column(u'payroll_entry', 'amount',
                      self.gf('django.db.models.fields.FloatField')(default=None),
                      keep_default=False)

        # Adding field 'Entry.sn'
        db.add_column(u'payroll_entry', 'sn',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)

        # Adding field 'Entry.employee'
        db.add_column(u'payroll_entry', 'employee',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Account']),
                      keep_default=False)


    models = {
        u'core.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'tag'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'ledger.account': {
            'Meta': {'object_name': 'Account'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['core.Tag']"})
        },
        u'payroll.entry': {
            'Meta': {'object_name': 'Entry'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'payroll.entryrow': {
            'Meta': {'object_name': 'EntryRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Entry']"}),
            'hours': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pay_heading': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['payroll']