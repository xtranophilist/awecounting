from rest_framework import serializers
from payroll.models import Entry, EntryRow


class EntryRowSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='employee_id')

    class Meta:
        model = EntryRow


class EntrySerializer(serializers.ModelSerializer):
    rows = EntryRowSerializer()

    class Meta:
        model = Entry
        exclude = ['company']
