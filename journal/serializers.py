from rest_framework import serializers
from journal.models import DayJournal, DayCashSales


class DayCashSalesSerializer(serializers.ModelSerializer):
    item = serializers.Field(source='item.name')
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = DayCashSales
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    day_cash_sales = DayCashSalesSerializer()

    class Meta:
        model = DayJournal
        # depth = 1


