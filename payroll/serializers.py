from rest_framework import serializers
from payroll.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
