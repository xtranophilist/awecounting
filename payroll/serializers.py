from rest_framework import serializers
from payroll.models import Entry, EntryRow, AttendanceVoucher, Employee, WorkTimeVoucher


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


class WorkTimeVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTimeVoucher
        exclude = ['company']
