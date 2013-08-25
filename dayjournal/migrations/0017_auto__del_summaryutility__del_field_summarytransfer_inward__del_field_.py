# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SummaryUtility'
        db.delete_table(u'dayjournal_summaryutility')

        # Deleting field 'SummaryTransfer.inward'
        db.delete_column(u'dayjournal_summarytransfer', 'inward')

        # Deleting field 'SummaryTransfer.outward'
        db.delete_column(u'dayjournal_summarytransfer', 'outward')

        # Adding field 'SummaryTransfer.cash'
        db.add_column(u'dayjournal_summarytransfer', 'cash',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SummaryTransfer.cheque'
        db.add_column(u'dayjournal_summarytransfer', 'cheque',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SummaryTransfer.card'
        db.add_column(u'dayjournal_summarytransfer', 'card',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'SummaryUtility'
        db.create_table(u'dayjournal_summaryutility', (
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='summary_utility', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['SummaryUtility'])

        # Adding field 'SummaryTransfer.inward'
        db.add_column(u'dayjournal_summarytransfer', 'inward',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'SummaryTransfer.outward'
        db.add_column(u'dayjournal_summarytransfer', 'outward',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'SummaryTransfer.cash'
        db.delete_column(u'dayjournal_summarytransfer', 'cash')

        # Deleting field 'SummaryTransfer.cheque'
        db.delete_column(u'dayjournal_summarytransfer', 'cheque')

        # Deleting field 'SummaryTransfer.card'
        db.delete_column(u'dayjournal_summarytransfer', 'card')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_tax': ('django.db.models.fields.FloatField', [], {})
        },
        u'dayjournal.lottodetailrow': {
            'Meta': {'object_name': 'LottoDetailRow'},
            'actual_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lotto_details'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_pack': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'purchase_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'sold_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'})
        },
        u'dayjournal.summarybank': {
            'Meta': {'object_name': 'SummaryBank'},
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'cash_deposit': ('django.db.models.fields.FloatField', [], {}),
            'cheque_deposit': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_bank'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarycash': {
            'Meta': {'object_name': 'SummaryCash'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
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
            'actual': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_inventory'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.InventoryAccount']"}),
            'purchase': ('django.db.models.fields.IntegerField', [], {}),
            'sales': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarylotto': {
            'Meta': {'object_name': 'SummaryLotto'},
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_lotto'", 'to': u"orm['dayjournal.DayJournal']"}),
            'disp': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'reg': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarytransfer': {
            'Meta': {'object_name': 'SummaryTransfer'},
            'card': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cash': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cheque': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_transfer'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transfer_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'inventory.inventoryaccount': {
            'Meta': {'object_name': 'InventoryAccount'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['dayjournal']