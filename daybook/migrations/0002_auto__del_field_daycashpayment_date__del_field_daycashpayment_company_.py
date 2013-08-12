# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DayCashPayment.date'
        db.delete_column(u'journal_daycashpayment', 'date')

        # Deleting field 'DayCashPayment.company'
        db.delete_column(u'journal_daycashpayment', 'company_id')

        # Deleting field 'DayCreditSales.date'
        db.delete_column(u'journal_daycreditsales', 'date')

        # Deleting field 'DayCreditSales.company'
        db.delete_column(u'journal_daycreditsales', 'company_id')

        # Deleting field 'DayCreditExpense.date'
        db.delete_column(u'journal_daycreditexpense', 'date')

        # Deleting field 'DayCreditExpense.company'
        db.delete_column(u'journal_daycreditexpense', 'company_id')

        # Deleting field 'DayCashSales.date'
        db.delete_column(u'journal_daycashsales', 'date')

        # Deleting field 'DayCashSales.company'
        db.delete_column(u'journal_daycashsales', 'company_id')

        # Deleting field 'DayCreditPurchase.date'
        db.delete_column(u'journal_daycreditpurchase', 'date')

        # Deleting field 'DayCreditPurchase.company'
        db.delete_column(u'journal_daycreditpurchase', 'company_id')

        # Deleting field 'DayCreditIncome.date'
        db.delete_column(u'journal_daycreditincome', 'date')

        # Deleting field 'DayCreditIncome.company'
        db.delete_column(u'journal_daycreditincome', 'company_id')

        # Deleting field 'DayCashReceipt.company'
        db.delete_column(u'journal_daycashreceipt', 'company_id')

        # Deleting field 'DayCashReceipt.date'
        db.delete_column(u'journal_daycashreceipt', 'date')

        # Deleting field 'DaySummaryEquivalent.date'
        db.delete_column(u'journal_daysummaryequivalent', 'date')

        # Deleting field 'DaySummaryEquivalent.company'
        db.delete_column(u'journal_daysummaryequivalent', 'company_id')

        # Deleting field 'DaySummaryCash.date'
        db.delete_column(u'journal_daysummarycash', 'date')

        # Deleting field 'DaySummaryCash.company'
        db.delete_column(u'journal_daysummarycash', 'company_id')

        # Deleting field 'DayCashPurchase.date'
        db.delete_column(u'journal_daycashpurchase', 'date')

        # Deleting field 'DayCashPurchase.company'
        db.delete_column(u'journal_daycashpurchase', 'company_id')


    def backwards(self, orm):
        # Adding field 'DayCashPayment.date'
        db.add_column(u'journal_daycashpayment', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCashPayment.company'
        db.add_column(u'journal_daycashpayment', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCreditSales.date'
        db.add_column(u'journal_daycreditsales', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCreditSales.company'
        db.add_column(u'journal_daycreditsales', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCreditExpense.date'
        db.add_column(u'journal_daycreditexpense', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCreditExpense.company'
        db.add_column(u'journal_daycreditexpense', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCashSales.date'
        db.add_column(u'journal_daycashsales', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCashSales.company'
        db.add_column(u'journal_daycashsales', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCreditPurchase.date'
        db.add_column(u'journal_daycreditpurchase', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCreditPurchase.company'
        db.add_column(u'journal_daycreditpurchase', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCreditIncome.date'
        db.add_column(u'journal_daycreditincome', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCreditIncome.company'
        db.add_column(u'journal_daycreditincome', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCashReceipt.company'
        db.add_column(u'journal_daycashreceipt', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCashReceipt.date'
        db.add_column(u'journal_daycashreceipt', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DaySummaryEquivalent.date'
        db.add_column(u'journal_daysummaryequivalent', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DaySummaryEquivalent.company'
        db.add_column(u'journal_daysummaryequivalent', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DaySummaryCash.date'
        db.add_column(u'journal_daysummarycash', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DaySummaryCash.company'
        db.add_column(u'journal_daysummarycash', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)

        # Adding field 'DayCashPurchase.date'
        db.add_column(u'journal_daycashpurchase', 'date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'DayCashPurchase.company'
        db.add_column(u'journal_daycashpurchase', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company']),
                      keep_default=False)


    models = {
        u'core.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'ac_no': ('django.db.models.fields.IntegerField', [], {}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'branch_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'purchase_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_items'", 'to': u"orm['ledger.Account']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'purchase_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_items'", 'to': u"orm['tax.TaxScheme']"}),
            'sales_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_items'", 'to': u"orm['ledger.Account']"}),
            'sales_price': ('django.db.models.fields.FloatField', [], {}),
            'sales_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_items'", 'to': u"orm['tax.TaxScheme']"})
        },
        u'journal.daycashpayment': {
            'Meta': {'object_name': 'DayCashPayment'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycashpurchase': {
            'Meta': {'object_name': 'DayCashPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycashreceipt': {
            'Meta': {'object_name': 'DayCashReceipt'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycashsales': {
            'Meta': {'object_name': 'DayCashSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycreditexpense': {
            'Meta': {'object_name': 'DayCreditExpense'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycreditincome': {
            'Meta': {'object_name': 'DayCreditIncome'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycreditpurchase': {
            'Meta': {'object_name': 'DayCreditPurchase'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daycreditsales': {
            'Meta': {'object_name': 'DayCreditSales'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daypayroll': {
            'Meta': {'object_name': 'DayPayroll'},
            'head': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax': ('django.db.models.fields.FloatField', [], {}),
            'total_taxable': ('django.db.models.fields.FloatField', [], {})
        },
        u'journal.daysummarybank': {
            'Meta': {'object_name': 'DaySummaryBank'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BankAccount']"}),
            'actual': ('django.db.models.fields.FloatField', [], {}),
            'collection': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_and_commission': ('django.db.models.fields.FloatField', [], {}),
            'interest_receipt': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'withdrawal': ('django.db.models.fields.FloatField', [], {})
        },
        u'journal.daysummarycash': {
            'Meta': {'object_name': 'DaySummaryCash'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'journal.daysummaryequivalent': {
            'Meta': {'object_name': 'DaySummaryEquivalent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inward': ('django.db.models.fields.FloatField', [], {}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'outward': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daysummaryinventory': {
            'Meta': {'object_name': 'DaySummaryInventory'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'purchase': ('django.db.models.fields.FloatField', [], {}),
            'sales': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'journal.daysummarysalestax': {
            'Meta': {'object_name': 'DaySummarySalesTax'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tax.TaxScheme']"})
        },
        u'ledger.account': {
            'Meta': {'object_name': 'Account'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        }
    }

    complete_apps = ['journal']