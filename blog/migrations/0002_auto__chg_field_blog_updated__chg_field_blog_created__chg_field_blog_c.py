# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Blog.updated'
        db.alter_column(u'blog_blog', 'updated', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Blog.created'
        db.alter_column(u'blog_blog', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Blog.content'
        db.alter_column(u'blog_blog', 'content', self.gf('redactor.fields.RedactorField')())

    def backwards(self, orm):

        # Changing field 'Blog.updated'
        db.alter_column(u'blog_blog', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Blog.created'
        db.alter_column(u'blog_blog', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Blog.content'
        db.alter_column(u'blog_blog', 'content', self.gf('django.db.models.fields.TextField')())

    models = {
        u'blog.blog': {
            'Meta': {'object_name': 'Blog'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'content': ('redactor.fields.RedactorField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'users.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '245'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '245', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['blog']