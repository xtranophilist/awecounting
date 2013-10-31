from rest_framework import serializers
from payroll.models import Entry, EntryRow, AttendanceVoucher, Employee, WorkTimeVoucher, WorkTimeVoucherRow, WorkDay, GroupPayroll, GroupPayrollRow, IndividualPayroll, Inclusion


class EntryRowSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='employee_id')

    class Meta:
        model = EntryRow


class EntrySerializer(serializers.ModelSerializer):
    rows = EntryRowSerializer()

    class Meta:
        model = Entry
        exclude = ['company']


class EmployeeSerializer(serializers.ModelSerializer):
    text = serializers.Field(source='name')
    unpaid_days = serializers.Field(source='get_unpaid_days')
    unpaid_hours = serializers.Field(source='get_unpaid_hours')
    unpaid_ot_hours = serializers.Field(source='get_unpaid_ot_hours')

    class Meta:
        model = Employee
        fields = ['text', 'id', 'tax_id', 'unpaid_days', 'unpaid_hours', 'unpaid_ot_hours']


class AttendanceVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceVoucher
        exclude = ['company']


class WorkDaySerializer(serializers.ModelSerializer):
    in_time = serializers.Field(source='get_in_time')
    out_time = serializers.Field(source='get_out_time')

    class Meta:
        model = WorkDay
        exclude = ['work_time_voucher_row']


class WorkTimeVoucherRowSerializer(serializers.ModelSerializer):
    work_days = WorkDaySerializer()

    class Meta:
        model = WorkTimeVoucherRow
        exclude = ['work_time_voucher']


class WorkTimeVoucherSerializer(serializers.ModelSerializer):
    rows = WorkTimeVoucherRowSerializer()

    class Meta:
        model = WorkTimeVoucher
        exclude = ['company']


class GroupPayrollRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPayrollRow


class GroupPayrollSerializer(serializers.ModelSerializer):
    rows = GroupPayrollRowSerializer()

    class Meta:
        model = GroupPayroll


class InclusionSerializer(serializers.ModelSerializer):
    account = serializers.Field(source='particular.id')

    class Meta:
        model = Inclusion


class DeductionSerializer(serializers.ModelSerializer):
    account = serializers.Field(source='particular.id')

    class Meta:
        model = Inclusion


class IndividualPayrollSerializer(serializers.ModelSerializer):
    inclusions = InclusionSerializer()
    deductions = DeductionSerializer()

    class Meta:
        model = IndividualPayroll
