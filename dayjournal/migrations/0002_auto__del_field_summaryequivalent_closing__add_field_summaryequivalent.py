# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SummaryEquivalent.closing'
        db.delete_column(u'dayjournal_summaryequivalent', 'closing')

        # Adding field 'SummaryEquivalent.actual'
        db.add_column(u'dayjournal_summaryequivalent', 'actual',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SummaryEquivalent.closing'
        db.add_column(u'dayjournal_summaryequivalent', 'closing',
                      self.gf('django.db.models.fields.FloatField')(default=None),
                      keep_default=False)

        # Deleting field 'SummaryEquivalent.actual'
        db.delete_column(u'dayjournal_summaryequivalent', 'actual')


    models = {
        u'dayjournal.cashpayment': {
            'Meta': {'object_name': 'CashPayment'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_payment'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashpurchase': {
            'Meta': {'object_name': 'CashPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_purchase'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashreceipt': {
            'Meta': {'object_name': 'CashReceipt'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_receipt'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashsales': {
            'Meta': {'object_name': 'CashSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.creditexpense': {
            'Meta': {'object_name': 'CreditExpense'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_expense'", 'to': u"orm['dayjournal.DayJournal']"}),
            'expense_claimed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expense_claimed_by'", 'to': u"orm['ledger.Account']"}),
            'expense_head': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expense_head'", 'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.creditincome': {
            'Meta': {'object_name': 'CreditIncome'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_income'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'income_from'", 'to': u"orm['ledger.Account']"}),
            'income_head': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'income_head'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.creditpurchase': {
            'Meta': {'object_name': 'CreditPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_purchase'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_ledger'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier'", 'to': u"orm['ledger.Account']"})
        },
        u'dayjournal.creditsales': {
            'Meta': {'object_name': 'CreditSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customer'", 'to': u"orm['ledger.Account']"}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_ledger'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.dayjournal': {
            'Meta': {'object_name': 'DayJournal', 'db_table': "'day_journal'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.summarybank': {
            'Meta': {'object_name': 'SummaryBank'},
            'account_transfer_minus': ('django.db.models.fields.FloatField', [], {}),
            'account_transfer_plus': ('django.db.models.fields.FloatField', [], {}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'card_deposit': ('django.db.models.fields.FloatField', [], {}),
            'cash_deposit': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_bank'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarycash': {
            'Meta': {'object_name': 'SummaryCash'},
            'closing': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_cash'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.summaryequivalent': {
            'Meta': {'object_name': 'SummaryEquivalent'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_equivalent'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inward': ('django.db.models.fields.FloatField', [], {}),
            'outward': ('django.db.models.fields.FloatField', [], {}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summaryinventory': {
            'Meta': {'object_name': 'SummaryInventory'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_inventory'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'purchase': ('django.db.models.fields.FloatField', [], {}),
            'sales': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarysalestax': {
            'Meta': {'object_name': 'SummarySalesTax'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_sales_tax'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'dayjournal.summarytransfer': {
            'Meta': {'object_name': 'SummaryTransfer'},
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_transfer'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inward': ('django.db.models.fields.FloatField', [], {}),
            'outward': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transfer_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'ledger.account': {
            'Meta': {'object_name': 'Account'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['dayjournal']
