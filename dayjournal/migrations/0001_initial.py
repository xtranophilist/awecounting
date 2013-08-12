# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DayBook'
        db.create_table('day_journal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
        ))
        db.send_create_signal(u'dayjournal', ['DayBook'])

        # Adding model 'CashSales'
        db.create_table(u'dayjournal_cashsales', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('sales_ledger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_sales', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CashSales'])

        # Adding model 'CashPurchase'
        db.create_table(u'dayjournal_cashpurchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('purchase_ledger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_purchase', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CashPurchase'])

        # Adding model 'CashReceipt'
        db.create_table(u'dayjournal_cashreceipt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('received_from', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_receipt', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CashReceipt'])

        # Adding model 'CashPayment'
        db.create_table(u'dayjournal_cashpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('payment_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_payment', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CashPayment'])

        # Adding model 'CreditSales'
        db.create_table(u'dayjournal_creditsales', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('sales_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sales_ledger', to=orm['ledger.Account'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customer', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_sales', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CreditSales'])

        # Adding model 'CreditPurchase'
        db.create_table(u'dayjournal_creditpurchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('purchase_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_ledger', to=orm['ledger.Account'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supplier', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_purchase', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CreditPurchase'])

        # Adding model 'CreditExpense'
        db.create_table(u'dayjournal_creditexpense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('expense_head', self.gf('django.db.models.fields.related.ForeignKey')(related_name='expense_head', to=orm['ledger.Account'])),
            ('expense_claimed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='expense_claimed_by', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_expense', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CreditExpense'])

        # Adding model 'CreditIncome'
        db.create_table(u'dayjournal_creditincome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('income_head', self.gf('django.db.models.fields.related.ForeignKey')(related_name='income_head', to=orm['ledger.Account'])),
            ('income_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='income_from', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_income', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['CreditIncome'])

        # Adding model 'SummaryCash'
        db.create_table(u'dayjournal_summarycash', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('closing', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_cash', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['SummaryCash'])

        # Adding model 'SummaryEquivalent'
        db.create_table(u'dayjournal_summaryequivalent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('particular', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('inward', self.gf('django.db.models.fields.FloatField')()),
            ('outward', self.gf('django.db.models.fields.FloatField')()),
            ('closing', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_equivalent', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['SummaryEquivalent'])

        # Adding model 'SummaryTransfer'
        db.create_table(u'dayjournal_summarytransfer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('transfer_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('inward', self.gf('django.db.models.fields.FloatField')()),
            ('outward', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_transfer', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['SummaryTransfer'])

        # Adding model 'SummaryBank'
        db.create_table(u'dayjournal_summarybank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('card_deposit', self.gf('django.db.models.fields.FloatField')()),
            ('cash_deposit', self.gf('django.db.models.fields.FloatField')()),
            ('account_transfer_plus', self.gf('django.db.models.fields.FloatField')()),
            ('account_transfer_minus', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_bank', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['SummaryBank'])

        # Adding model 'SummarySalesTax'
        db.create_table(u'dayjournal_summarysalestax', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_sales_tax', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['SummarySalesTax'])

        # Adding model 'SummaryInventory'
        db.create_table(u'dayjournal_summaryinventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('particular', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('purchase', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.FloatField')()),
            ('actual', self.gf('django.db.models.fields.FloatField')()),
            ('day_book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_inventory', to=orm['dayjournal.DayBook'])),
        ))
        db.send_create_signal(u'dayjournal', ['SummaryInventory'])


    def backwards(self, orm):
        # Deleting model 'DayBook'
        db.delete_table('day_journal')

        # Deleting model 'CashSales'
        db.delete_table(u'dayjournal_cashsales')

        # Deleting model 'CashPurchase'
        db.delete_table(u'dayjournal_cashpurchase')

        # Deleting model 'CashReceipt'
        db.delete_table(u'dayjournal_cashreceipt')

        # Deleting model 'CashPayment'
        db.delete_table(u'dayjournal_cashpayment')

        # Deleting model 'CreditSales'
        db.delete_table(u'dayjournal_creditsales')

        # Deleting model 'CreditPurchase'
        db.delete_table(u'dayjournal_creditpurchase')

        # Deleting model 'CreditExpense'
        db.delete_table(u'dayjournal_creditexpense')

        # Deleting model 'CreditIncome'
        db.delete_table(u'dayjournal_creditincome')

        # Deleting model 'SummaryCash'
        db.delete_table(u'dayjournal_summarycash')

        # Deleting model 'SummaryEquivalent'
        db.delete_table(u'dayjournal_summaryequivalent')

        # Deleting model 'SummaryTransfer'
        db.delete_table(u'dayjournal_summarytransfer')

        # Deleting model 'SummaryBank'
        db.delete_table(u'dayjournal_summarybank')

        # Deleting model 'SummarySalesTax'
        db.delete_table(u'dayjournal_summarysalestax')

        # Deleting model 'SummaryInventory'
        db.delete_table(u'dayjournal_summaryinventory')


    models = {
        u'dayjournal.cashpayment': {
            'Meta': {'object_name': 'CashPayment'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_payment'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashpurchase': {
            'Meta': {'object_name': 'CashPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_purchase'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashreceipt': {
            'Meta': {'object_name': 'CashReceipt'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_receipt'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashsales': {
            'Meta': {'object_name': 'CashSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_sales'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.creditexpense': {
            'Meta': {'object_name': 'CreditExpense'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_expense'", 'to': u"orm['dayjournal.DayBook']"}),
            'expense_claimed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expense_claimed_by'", 'to': u"orm['ledger.Account']"}),
            'expense_head': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expense_head'", 'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.creditincome': {
            'Meta': {'object_name': 'CreditIncome'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_income'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'income_from'", 'to': u"orm['ledger.Account']"}),
            'income_head': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'income_head'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.creditpurchase': {
            'Meta': {'object_name': 'CreditPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_purchase'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_ledger'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier'", 'to': u"orm['ledger.Account']"})
        },
        u'dayjournal.creditsales': {
            'Meta': {'object_name': 'CreditSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customer'", 'to': u"orm['ledger.Account']"}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credit_sales'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_ledger'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.daybook': {
            'Meta': {'object_name': 'DayBook', 'db_table': "'day_journal'"},
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
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_bank'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarycash': {
            'Meta': {'object_name': 'SummaryCash'},
            'closing': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_cash'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.summaryequivalent': {
            'Meta': {'object_name': 'SummaryEquivalent'},
            'closing': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_equivalent'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inward': ('django.db.models.fields.FloatField', [], {}),
            'outward': ('django.db.models.fields.FloatField', [], {}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summaryinventory': {
            'Meta': {'object_name': 'SummaryInventory'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_inventory'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'purchase': ('django.db.models.fields.FloatField', [], {}),
            'sales': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarysalestax': {
            'Meta': {'object_name': 'SummarySalesTax'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_sales_tax'", 'to': u"orm['dayjournal.DayBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'dayjournal.summarytransfer': {
            'Meta': {'object_name': 'SummaryTransfer'},
            'day_book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_transfer'", 'to': u"orm['dayjournal.DayBook']"}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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