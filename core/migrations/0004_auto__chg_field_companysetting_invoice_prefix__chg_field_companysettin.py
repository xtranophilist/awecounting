# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CompanySetting.invoice_prefix'
        db.alter_column(u'core_companysetting', 'invoice_prefix', self.gf('django.db.models.fields.CharField')(max_length=5, null=True))

        # Changing field 'CompanySetting.invoice_suffix'
        db.alter_column(u'core_companysetting', 'invoice_suffix', self.gf('django.db.models.fields.CharField')(max_length=5, null=True))

    def backwards(self, orm):

        # Changing field 'CompanySetting.invoice_prefix'
        db.alter_column(u'core_companysetting', 'invoice_prefix', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'CompanySetting.invoice_suffix'
        db.alter_column(u'core_companysetting', 'invoice_suffix', self.gf('django.db.models.fields.CharField')(max_length=5))

    models = {
        u'core.companysetting': {
            'Meta': {'object_name': 'CompanySetting'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'default_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_digit_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'invoice_prefix': ('django.db.models.fields.CharField', [], {'default': "'INV-'", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'invoice_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
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
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['core']