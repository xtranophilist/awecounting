from rest_framework import serializers
from payroll.models import Entry, EntryRow, AttendanceVoucher, Employee, WorkTimeVoucher, WorkTimeVoucherRow, WorkDay


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

    class Meta:
        model = Employee
        exclude = ['company', 'address', 'designation', 'account', 'name']


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

