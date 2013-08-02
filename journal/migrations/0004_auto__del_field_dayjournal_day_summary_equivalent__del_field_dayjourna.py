# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DayJournal.day_summary_equivalent'
        db.delete_column('journal_day', 'day_summary_equivalent_id')

        # Deleting field 'DayJournal.day_cash_sales'
        db.delete_column('journal_day', 'day_cash_sales_id')

        # Deleting field 'DayJournal.day_cash_receipt'
        db.delete_column('journal_day', 'day_cash_receipt_id')

        # Deleting field 'DayJournal.day_cash_payment'
        db.delete_column('journal_day', 'day_cash_payment_id')

        # Deleting field 'DayJournal.day_credit_expense'
        db.delete_column('journal_day', 'day_credit_expense_id')

        # Deleting field 'DayJournal.day_cash_purchase'
        db.delete_column('journal_day', 'day_cash_purchase_id')

        # Deleting field 'DayJournal.day_summary_bank'
        db.delete_column('journal_day', 'day_summary_bank_id')

        # Deleting field 'DayJournal.day_summary_inventory'
        db.delete_column('journal_day', 'day_summary_inventory_id')

        # Deleting field 'DayJournal.day_credit_income'
        db.delete_column('journal_day', 'day_credit_income_id')

        # Deleting field 'DayJournal.day_summary_sales_tax'
        db.delete_column('journal_day', 'day_summary_sales_tax_id')

        # Deleting field 'DayJournal.day_payroll'
        db.delete_column('journal_day', 'day_payroll_id')

        # Deleting field 'DayJournal.day_credit_sales'
        db.delete_column('journal_day', 'day_credit_sales_id')

        # Deleting field 'DayJournal.day_credit_purchase'
        db.delete_column('journal_day', 'day_credit_purchase_id')

        # Adding M2M table for field day_cash_sales on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_cash_sales')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycashsales', models.ForeignKey(orm[u'journal.daycashsales'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycashsales_id'])

        # Adding M2M table for field day_cash_purchase on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_cash_purchase')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycashpurchase', models.ForeignKey(orm[u'journal.daycashpurchase'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycashpurchase_id'])

        # Adding M2M table for field day_cash_receipt on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_cash_receipt')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycashreceipt', models.ForeignKey(orm[u'journal.daycashreceipt'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycashreceipt_id'])

        # Adding M2M table for field day_cash_payment on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_cash_payment')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycashpayment', models.ForeignKey(orm[u'journal.daycashpayment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycashpayment_id'])

        # Adding M2M table for field day_credit_sales on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_credit_sales')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycreditsales', models.ForeignKey(orm[u'journal.daycreditsales'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycreditsales_id'])

        # Adding M2M table for field day_credit_purchase on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_credit_purchase')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycreditpurchase', models.ForeignKey(orm[u'journal.daycreditpurchase'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycreditpurchase_id'])

        # Adding M2M table for field day_credit_expense on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_credit_expense')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycreditexpense', models.ForeignKey(orm[u'journal.daycreditexpense'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycreditexpense_id'])

        # Adding M2M table for field day_credit_income on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_credit_income')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daycreditincome', models.ForeignKey(orm[u'journal.daycreditincome'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daycreditincome_id'])

        # Adding M2M table for field day_summary_equivalent on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_summary_equivalent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daysummaryequivalent', models.ForeignKey(orm[u'journal.daysummaryequivalent'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daysummaryequivalent_id'])

        # Adding M2M table for field day_summary_bank on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_summary_bank')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daysummarybank', models.ForeignKey(orm[u'journal.daysummarybank'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daysummarybank_id'])

        # Adding M2M table for field day_summary_sales_tax on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_summary_sales_tax')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daysummarysalestax', models.ForeignKey(orm[u'journal.daysummarysalestax'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daysummarysalestax_id'])

        # Adding M2M table for field day_summary_inventory on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_summary_inventory')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daysummaryinventory', models.ForeignKey(orm[u'journal.daysummaryinventory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daysummaryinventory_id'])

        # Adding M2M table for field day_payroll on 'DayJournal'
        m2m_table_name = db.shorten_name('journal_day_day_payroll')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dayjournal', models.ForeignKey(orm[u'journal.dayjournal'], null=False)),
            ('daypayroll', models.ForeignKey(orm[u'journal.daypayroll'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dayjournal_id', 'daypayroll_id'])


    def backwards(self, orm):
        # Adding field 'DayJournal.day_summary_equivalent'
        db.add_column('journal_day', 'day_summary_equivalent',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DaySummaryEquivalent']),
                      keep_default=False)

        # Adding field 'DayJournal.day_cash_sales'
        db.add_column('journal_day', 'day_cash_sales',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCashSales']),
                      keep_default=False)

        # Adding field 'DayJournal.day_cash_receipt'
        db.add_column('journal_day', 'day_cash_receipt',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCashReceipt']),
                      keep_default=False)

        # Adding field 'DayJournal.day_cash_payment'
        db.add_column('journal_day', 'day_cash_payment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCashPayment']),
                      keep_default=False)

        # Adding field 'DayJournal.day_credit_expense'
        db.add_column('journal_day', 'day_credit_expense',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCreditExpense']),
                      keep_default=False)

        # Adding field 'DayJournal.day_cash_purchase'
        db.add_column('journal_day', 'day_cash_purchase',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCashPurchase']),
                      keep_default=False)

        # Adding field 'DayJournal.day_summary_bank'
        db.add_column('journal_day', 'day_summary_bank',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DaySummaryBank']),
                      keep_default=False)

        # Adding field 'DayJournal.day_summary_inventory'
        db.add_column('journal_day', 'day_summary_inventory',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DaySummaryInventory']),
                      keep_default=False)

        # Adding field 'DayJournal.day_credit_income'
        db.add_column('journal_day', 'day_credit_income',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCreditIncome']),
                      keep_default=False)

        # Adding field 'DayJournal.day_summary_sales_tax'
        db.add_column('journal_day', 'day_summary_sales_tax',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DaySummarySalesTax']),
                      keep_default=False)

        # Adding field 'DayJournal.day_payroll'
        db.add_column('journal_day', 'day_payroll',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayPayroll']),
                      keep_default=False)

        # Adding field 'DayJournal.day_credit_sales'
        db.add_column('journal_day', 'day_credit_sales',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCreditSales']),
                      keep_default=False)

        # Adding field 'DayJournal.day_credit_purchase'
        db.add_column('journal_day', 'day_credit_purchase',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['journal.DayCreditPurchase']),
                      keep_default=False)

        # Removing M2M table for field day_cash_sales on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_cash_sales'))

        # Removing M2M table for field day_cash_purchase on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_cash_purchase'))

        # Removing M2M table for field day_cash_receipt on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_cash_receipt'))

        # Removing M2M table for field day_cash_payment on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_cash_payment'))

        # Removing M2M table for field day_credit_sales on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_credit_sales'))

        # Removing M2M table for field day_credit_purchase on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_credit_purchase'))

        # Removing M2M table for field day_credit_expense on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_credit_expense'))

        # Removing M2M table for field day_credit_income on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_credit_income'))

        # Removing M2M table for field day_summary_equivalent on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_summary_equivalent'))

        # Removing M2M table for field day_summary_bank on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_summary_bank'))

        # Removing M2M table for field day_summary_sales_tax on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_summary_sales_tax'))

        # Removing M2M table for field day_summary_inventory on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_summary_inventory'))

        # Removing M2M table for field day_payroll on 'DayJournal'
        db.delete_table(db.shorten_name('journal_day_day_payroll'))


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
        u'journal.dayjournal': {
            'Meta': {'object_name': 'DayJournal', 'db_table': "'journal_day'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day_cash_payment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCashPayment']", 'symmetrical': 'False'}),
            'day_cash_purchase': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCashPurchase']", 'symmetrical': 'False'}),
            'day_cash_receipt': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCashReceipt']", 'symmetrical': 'False'}),
            'day_cash_sales': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCashSales']", 'symmetrical': 'False'}),
            'day_credit_expense': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCreditExpense']", 'symmetrical': 'False'}),
            'day_credit_income': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCreditIncome']", 'symmetrical': 'False'}),
            'day_credit_purchase': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCreditPurchase']", 'symmetrical': 'False'}),
            'day_credit_sales': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayCreditSales']", 'symmetrical': 'False'}),
            'day_payroll': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DayPayroll']", 'symmetrical': 'False'}),
            'day_summary_bank': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DaySummaryBank']", 'symmetrical': 'False'}),
            'day_summary_cash': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.DaySummaryCash']"}),
            'day_summary_equivalent': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DaySummaryEquivalent']", 'symmetrical': 'False'}),
            'day_summary_inventory': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DaySummaryInventory']", 'symmetrical': 'False'}),
            'day_summary_sales_tax': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.DaySummarySalesTax']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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