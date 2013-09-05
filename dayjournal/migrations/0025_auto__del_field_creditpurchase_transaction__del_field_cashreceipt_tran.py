# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding M2M table for field transactions on 'CashEquivalentSales'
        m2m_table_name = db.shorten_name(u'dayjournal_cashequivalentsales_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cashequivalentsales', models.ForeignKey(orm[u'dayjournal.cashequivalentsales'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cashequivalentsales_id', 'transaction_id'])

        # Deleting field 'CreditPurchase.transaction'
        db.delete_column(u'dayjournal_creditpurchase', 'transaction_id')

        # Adding M2M table for field transactions on 'CreditPurchase'
        m2m_table_name = db.shorten_name(u'dayjournal_creditpurchase_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creditpurchase', models.ForeignKey(orm[u'dayjournal.creditpurchase'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creditpurchase_id', 'transaction_id'])

        # Adding M2M table for field transactions on 'ChequePurchase'
        m2m_table_name = db.shorten_name(u'dayjournal_chequepurchase_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chequepurchase', models.ForeignKey(orm[u'dayjournal.chequepurchase'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['chequepurchase_id', 'transaction_id'])

        # Adding M2M table for field transactions on 'CardSales'
        m2m_table_name = db.shorten_name(u'dayjournal_cardsales_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cardsales', models.ForeignKey(orm[u'dayjournal.cardsales'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cardsales_id', 'transaction_id'])

        # Deleting field 'CashReceipt.transaction'
        db.delete_column(u'dayjournal_cashreceipt', 'transaction_id')

        # Adding M2M table for field transactions on 'CashReceipt'
        m2m_table_name = db.shorten_name(u'dayjournal_cashreceipt_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cashreceipt', models.ForeignKey(orm[u'dayjournal.cashreceipt'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cashreceipt_id', 'transaction_id'])

        # Adding M2M table for field transactions on 'SummaryTransfer'
        m2m_table_name = db.shorten_name(u'dayjournal_summarytransfer_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('summarytransfer', models.ForeignKey(orm[u'dayjournal.summarytransfer'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['summarytransfer_id', 'transaction_id'])

        # Adding M2M table for field transactions on 'SummaryLotto'
        m2m_table_name = db.shorten_name(u'dayjournal_summarylotto_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('summarylotto', models.ForeignKey(orm[u'dayjournal.summarylotto'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['summarylotto_id', 'transaction_id'])

        # Deleting field 'CreditExpense.transaction'
        db.delete_column(u'dayjournal_creditexpense', 'transaction_id')

        # Adding M2M table for field transactions on 'CreditExpense'
        m2m_table_name = db.shorten_name(u'dayjournal_creditexpense_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creditexpense', models.ForeignKey(orm[u'dayjournal.creditexpense'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creditexpense_id', 'transaction_id'])

        # Deleting field 'CreditSales.transaction'
        db.delete_column(u'dayjournal_creditsales', 'transaction_id')

        # Adding M2M table for field transactions on 'CreditSales'
        m2m_table_name = db.shorten_name(u'dayjournal_creditsales_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creditsales', models.ForeignKey(orm[u'dayjournal.creditsales'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creditsales_id', 'transaction_id'])

        # Deleting field 'CreditIncome.transaction'
        db.delete_column(u'dayjournal_creditincome', 'transaction_id')

        # Adding M2M table for field transactions on 'CreditIncome'
        m2m_table_name = db.shorten_name(u'dayjournal_creditincome_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creditincome', models.ForeignKey(orm[u'dayjournal.creditincome'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creditincome_id', 'transaction_id'])

        # Adding M2M table for field transactions on 'SummaryBank'
        m2m_table_name = db.shorten_name(u'dayjournal_summarybank_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('summarybank', models.ForeignKey(orm[u'dayjournal.summarybank'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['summarybank_id', 'transaction_id'])

        # Deleting field 'CashPurchase.transaction'
        db.delete_column(u'dayjournal_cashpurchase', 'transaction_id')

        # Adding M2M table for field transactions on 'CashPurchase'
        m2m_table_name = db.shorten_name(u'dayjournal_cashpurchase_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cashpurchase', models.ForeignKey(orm[u'dayjournal.cashpurchase'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cashpurchase_id', 'transaction_id'])

        # Deleting field 'CashPayment.transaction'
        db.delete_column(u'dayjournal_cashpayment', 'transaction_id')

        # Adding M2M table for field transactions on 'CashPayment'
        m2m_table_name = db.shorten_name(u'dayjournal_cashpayment_transactions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cashpayment', models.ForeignKey(orm[u'dayjournal.cashpayment'], null=False)),
            ('transaction', models.ForeignKey(orm[u'ledger.transaction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cashpayment_id', 'transaction_id'])


    def backwards(self, orm):
        # Removing M2M table for field transactions on 'CashEquivalentSales'
        db.delete_table(db.shorten_name(u'dayjournal_cashequivalentsales_transactions'))

        # Adding field 'CreditPurchase.transaction'
        db.add_column(u'dayjournal_creditpurchase', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CreditPurchase'
        db.delete_table(db.shorten_name(u'dayjournal_creditpurchase_transactions'))

        # Removing M2M table for field transactions on 'ChequePurchase'
        db.delete_table(db.shorten_name(u'dayjournal_chequepurchase_transactions'))

        # Removing M2M table for field transactions on 'CardSales'
        db.delete_table(db.shorten_name(u'dayjournal_cardsales_transactions'))

        # Adding field 'CashReceipt.transaction'
        db.add_column(u'dayjournal_cashreceipt', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CashReceipt'
        db.delete_table(db.shorten_name(u'dayjournal_cashreceipt_transactions'))

        # Removing M2M table for field transactions on 'SummaryTransfer'
        db.delete_table(db.shorten_name(u'dayjournal_summarytransfer_transactions'))

        # Removing M2M table for field transactions on 'SummaryLotto'
        db.delete_table(db.shorten_name(u'dayjournal_summarylotto_transactions'))

        # Adding field 'CreditExpense.transaction'
        db.add_column(u'dayjournal_creditexpense', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CreditExpense'
        db.delete_table(db.shorten_name(u'dayjournal_creditexpense_transactions'))

        # Adding field 'CreditSales.transaction'
        db.add_column(u'dayjournal_creditsales', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CreditSales'
        db.delete_table(db.shorten_name(u'dayjournal_creditsales_transactions'))

        # Adding field 'CreditIncome.transaction'
        db.add_column(u'dayjournal_creditincome', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CreditIncome'
        db.delete_table(db.shorten_name(u'dayjournal_creditincome_transactions'))

        # Removing M2M table for field transactions on 'SummaryBank'
        db.delete_table(db.shorten_name(u'dayjournal_summarybank_transactions'))

        # Adding field 'CashPurchase.transaction'
        db.add_column(u'dayjournal_cashpurchase', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CashPurchase'
        db.delete_table(db.shorten_name(u'dayjournal_cashpurchase_transactions'))

        # Adding field 'CashPayment.transaction'
        db.add_column(u'dayjournal_cashpayment', 'transaction',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ledger.Transaction']),
                      keep_default=False)

        # Removing M2M table for field transactions on 'CashPayment'
        db.delete_table(db.shorten_name(u'dayjournal_cashpayment_transactions'))


    models = {
        u'dayjournal.cardsales': {
            'Meta': {'object_name': 'CardSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'commission_out': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'card_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.cashequivalentsales': {
            'Meta': {'object_name': 'CashEquivalentSales'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'cash_equivalent_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.cashpayment': {
            'Meta': {'object_name': 'CashPayment'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'cash_payment'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.cashpurchase': {
            'Meta': {'object_name': 'CashPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'cash_purchase'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.cashreceipt': {
            'Meta': {'object_name': 'CashReceipt'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'cash_receipt'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.cashsales': {
            'Meta': {'object_name': 'CashSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'cash_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.chequepurchase': {
            'Meta': {'object_name': 'ChequePurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'commission_in': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'cheque_purchase'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.creditexpense': {
            'Meta': {'object_name': 'CreditExpense'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'credit_expense'", 'to': u"orm['dayjournal.DayJournal']"}),
            'expense_claimed_by': ('django.db.models.fields.related.ForeignKey', [],
                                   {'related_name': "'expense_claimed_by'", 'to': u"orm['ledger.Account']"}),
            'expense_head': ('django.db.models.fields.related.ForeignKey', [],
                             {'related_name': "'expense_head'", 'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.creditincome': {
            'Meta': {'object_name': 'CreditIncome'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'credit_income'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income_from': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'income_from'", 'to': u"orm['ledger.Account']"}),
            'income_head': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'income_head'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.creditpurchase': {
            'Meta': {'object_name': 'CreditPurchase'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'credit_purchase'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [],
                                {'related_name': "'purchase_ledger'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'supplier'", 'to': u"orm['ledger.Account']"}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.creditsales': {
            'Meta': {'object_name': 'CreditSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'customer'", 'to': u"orm['ledger.Account']"}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'credit_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [],
                             {'related_name': "'sales_ledger'", 'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.dayjournal': {
            'Meta': {'object_name': 'DayJournal', 'db_table': "'day_journal'"},
            'cash_deposit': ('django.db.models.fields.FloatField', [], {}),
            'cash_withdrawal': ('django.db.models.fields.FloatField', [], {}),
            'cheque_deposit': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_tax': ('django.db.models.fields.FloatField', [], {})
        },
        u'dayjournal.lottodetailrow': {
            'Meta': {'object_name': 'LottoDetailRow'},
            'actual_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'lotto_details'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_pack': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'purchase_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'sold_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'})
        },
        u'dayjournal.summarybank': {
            'Meta': {'object_name': 'SummaryBank'},
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'cash_deposit': ('django.db.models.fields.FloatField', [], {}),
            'cheque_deposit': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'summary_bank'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.summarycash': {
            'Meta': {'object_name': 'SummaryCash'},
            'actual': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'summary_cash'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.summaryinventory': {
            'Meta': {'object_name': 'SummaryInventory'},
            'actual': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'summary_inventory'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.InventoryAccount']"}),
            'purchase': ('django.db.models.fields.IntegerField', [], {}),
            'sales': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarylotto': {
            'Meta': {'object_name': 'SummaryLotto'},
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'summary_lotto'", 'to': u"orm['dayjournal.DayJournal']"}),
            'disp': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'reg': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'})
        },
        u'dayjournal.summarytransfer': {
            'Meta': {'object_name': 'SummaryTransfer'},
            'card': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cash': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cheque': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'summary_transfer'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transactions': ('django.db.models.fields.related.ManyToManyField', [],
                             {'to': u"orm['ledger.Transaction']", 'symmetrical': 'False'}),
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
            'category': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [],
                       {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ledger.category': {
            'Meta': {'object_name': 'Category'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': (
            'django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True',
                                                          'to': u"orm['ledger.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'ledger.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'transactions'", 'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'current_balance': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
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