# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CreditPurchase'
        db.delete_table(u'dayjournal_creditpurchase')

        # Deleting model 'ChequePurchase'
        db.delete_table(u'dayjournal_chequepurchase')

        # Deleting model 'CashReceipt'
        db.delete_table(u'dayjournal_cashreceipt')

        # Deleting model 'CashPurchase'
        db.delete_table(u'dayjournal_cashpurchase')

        # Deleting model 'CreditExpense'
        db.delete_table(u'dayjournal_creditexpense')

        # Deleting model 'CreditSales'
        db.delete_table(u'dayjournal_creditsales')

        # Deleting model 'CreditIncome'
        db.delete_table(u'dayjournal_creditincome')

        # Deleting model 'CashPayment'
        db.delete_table(u'dayjournal_cashpayment')

        # Adding model 'VendorPayout'
        db.create_table(u'dayjournal_vendorpayout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vendor_payouts', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('purchase_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payouts', to=orm['ledger.Account'])),
            ('remarks', self.gf('django.db.models.fields.TextField')()),
            ('paid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='new', max_length=3)),
        ))
        db.send_create_signal(u'dayjournal', ['VendorPayout'])


    def backwards(self, orm):
        # Adding model 'CreditPurchase'
        db.create_table(u'dayjournal_creditpurchase', (
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_purchase', to=orm['dayjournal.DayJournal'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supplier', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('purchase_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_ledger', to=orm['ledger.Account'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['CreditPurchase'])

        # Adding model 'ChequePurchase'
        db.create_table(u'dayjournal_chequepurchase', (
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_purchase', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('commission_in', self.gf('django.db.models.fields.FloatField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['ChequePurchase'])

        # Adding model 'CashReceipt'
        db.create_table(u'dayjournal_cashreceipt', (
            ('received_from', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_receipt', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['CashReceipt'])

        # Adding model 'CashPurchase'
        db.create_table(u'dayjournal_cashpurchase', (
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_purchase', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('purchase_ledger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['CashPurchase'])

        # Adding model 'CreditExpense'
        db.create_table(u'dayjournal_creditexpense', (
            ('expense_claimed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='expense_claimed_by', to=orm['ledger.Account'])),
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_expense', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('expense_head', self.gf('django.db.models.fields.related.ForeignKey')(related_name='expense_head', to=orm['ledger.Account'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['CreditExpense'])

        # Adding model 'CreditSales'
        db.create_table(u'dayjournal_creditsales', (
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customer', to=orm['ledger.Account'])),
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_sales', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('sales_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sales_ledger', to=orm['ledger.Account'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['CreditSales'])

        # Adding model 'CreditIncome'
        db.create_table(u'dayjournal_creditincome', (
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credit_income', to=orm['dayjournal.DayJournal'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('income_head', self.gf('django.db.models.fields.related.ForeignKey')(related_name='income_head', to=orm['ledger.Account'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('income_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='income_from', to=orm['ledger.Account'])),
        ))
        db.send_create_signal(u'dayjournal', ['CreditIncome'])

        # Adding model 'CashPayment'
        db.create_table(u'dayjournal_cashpayment', (
            ('day_journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_payment', to=orm['dayjournal.DayJournal'])),
            ('payment_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dayjournal', ['CashPayment'])

        # Deleting model 'VendorPayout'
        db.delete_table(u'dayjournal_vendorpayout')


    models = {
        u'dayjournal.bankattachment': {
            'Meta': {'object_name': 'BankAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bank_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.cardsales': {
            'Meta': {'object_name': 'CardSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'commission_out': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.cashequivalentsales': {
            'Meta': {'object_name': 'CashEquivalentSales'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_equivalent_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'dayjournal.dayjournal': {
            'Meta': {'object_name': 'DayJournal', 'db_table': "'day_journal'"},
            'cash_actual': ('django.db.models.fields.FloatField', [], {}),
            'cash_deposit': ('django.db.models.fields.FloatField', [], {}),
            'cash_withdrawal': ('django.db.models.fields.FloatField', [], {}),
            'cheque_deposit': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lotto_sales_dispenser_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'lotto_sales_register_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sales_tax': ('django.db.models.fields.FloatField', [], {}),
            'scratch_off_sales_register_amount': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'dayjournal.inventoryfuel': {
            'Meta': {'object_name': 'InventoryFuel'},
            'actual': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_fuel'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.InventoryAccount']"}),
            'purchase': ('django.db.models.fields.IntegerField', [], {}),
            'sales': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.lottodetail': {
            'Meta': {'object_name': 'LottoDetail'},
            'addition': ('django.db.models.fields.IntegerField', [], {}),
            'day_close': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lotto_detail'", 'to': u"orm['dayjournal.DayJournal']"}),
            'day_open': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pack_count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.otherattachment': {
            'Meta': {'object_name': 'OtherAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.purchaseattachment': {
            'Meta': {'object_name': 'PurchaseAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.salesattachment': {
            'Meta': {'object_name': 'SalesAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'dayjournal.vendorpayout': {
            'Meta': {'object_name': 'VendorPayout'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payouts'", 'to': u"orm['ledger.Account']"}),
            'remarks': ('django.db.models.fields.TextField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '3'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendor_payouts'", 'to': u"orm['ledger.Account']"})
        },
        u'inventory.inventoryaccount': {
            'Meta': {'object_name': 'InventoryAccount'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_balance': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'ledger.account': {
            'Meta': {'unique_together': "(('company', 'name'), ('company', 'code'))", 'object_name': 'Account'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_cr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'opening_dr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ledger.category': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Category'},
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