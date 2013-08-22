# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tag.lft'
        db.add_column('tag', u'lft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'Tag.rght'
        db.add_column('tag', u'rght',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'Tag.tree_id'
        db.add_column('tag', u'tree_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'Tag.level'
        db.add_column('tag', u'level',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)


        # Changing field 'Tag.parent'
        db.alter_column('tag', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['core.Tag']))

    def backwards(self, orm):
        # Deleting field 'Tag.lft'
        db.delete_column('tag', u'lft')

        # Deleting field 'Tag.rght'
        db.delete_column('tag', u'rght')

        # Deleting field 'Tag.tree_id'
        db.delete_column('tag', u'tree_id')

        # Deleting field 'Tag.level'
        db.delete_column('tag', u'level')


        # Changing field 'Tag.parent'
        db.alter_column('tag', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['core.Tag']))

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
        u'core.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'tag'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['core.Tag']"}),
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

    complete_apps = ['core']