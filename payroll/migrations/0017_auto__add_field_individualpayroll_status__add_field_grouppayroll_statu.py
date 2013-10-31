# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IndividualPayroll.status'
        db.add_column(u'payroll_individualpayroll', 'status',
                      self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10),
                      keep_default=False)

        # Adding field 'GroupPayroll.status'
        db.add_column(u'payroll_grouppayroll', 'status',
                      self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'IndividualPayroll.status'
        db.delete_column(u'payroll_individualpayroll', 'status')

        # Deleting field 'GroupPayroll.status'
        db.delete_column(u'payroll_grouppayroll', 'status')


    models = {
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
        u'payroll.attendancevoucher': {
            'Meta': {'object_name': 'AttendanceVoucher'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'early_late_attendance_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'early_late_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'full_present_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'half_multiplier': ('django.db.models.fields.FloatField', [], {'default': '0.5', 'null': 'True', 'blank': 'True'}),
            'half_present_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'total_ot_hours': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_working_days': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'payroll.deduction': {
            'Meta': {'object_name': 'Deduction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deductions'", 'to': u"orm['payroll.IndividualPayroll']"}),
            'particular': ('django.db.models.fields.FloatField', [], {})
        },
        u'payroll.employee': {
            'Meta': {'object_name': 'Employee'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ledger.Account']", 'unique': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'tax_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'payroll.entry': {
            'Meta': {'object_name': 'Entry'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry_no': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'payroll.entryrow': {
            'Meta': {'object_name': 'EntryRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['payroll.Entry']"}),
            'hours': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pay_heading': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'row'", 'to': u"orm['ledger.Account']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax': ('django.db.models.fields.FloatField', [], {})
        },
        u'payroll.grouppayroll': {
            'Meta': {'object_name': 'GroupPayroll'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'payroll.grouppayrollrow': {
            'Meta': {'object_name': 'GroupPayrollRow'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            'group_payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['payroll.GroupPayroll']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pay_head': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'payroll_tax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rate_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rate_hour': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rate_ot_hour': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'payroll.inclusion': {
            'Meta': {'object_name': 'Inclusion'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inclusions'", 'to': u"orm['payroll.IndividualPayroll']"}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'payroll.individualpayroll': {
            'Meta': {'object_name': 'IndividualPayroll'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day_rate': ('django.db.models.fields.FloatField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            'hour_rate': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ot_hour_rate': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'payroll.workday': {
            'Meta': {'object_name': 'WorkDay'},
            'day': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_time': ('django.db.models.fields.TimeField', [], {}),
            'out_time': ('django.db.models.fields.TimeField', [], {}),
            'work_time_voucher_row': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'work_days'", 'to': u"orm['payroll.WorkTimeVoucherRow']"})
        },
        u'payroll.worktimevoucher': {
            'Meta': {'object_name': 'WorkTimeVoucher'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'payroll.worktimevoucherrow': {
            'Meta': {'object_name': 'WorkTimeVoucherRow'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_time_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['payroll.WorkTimeVoucher']"})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['payroll']