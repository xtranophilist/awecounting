# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaxScheme'
        db.create_table(u'tax_taxscheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('percent', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'tax', ['TaxScheme'])


    def backwards(self, orm):
        # Deleting model 'TaxScheme'
        db.delete_table(u'tax_taxscheme')


    models = {
        u'tax.taxscheme': {
            'Meta': {'object_name': 'TaxScheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'percent': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['tax']