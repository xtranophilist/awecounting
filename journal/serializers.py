from rest_framework import serializers
from journal.models import DayJournal, DayCashSales


class DayCashSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayCashSales


class DayJournalSerializer(serializers.ModelSerializer):
    # day_cash_sales = DayCashSalesSerializer()

    class Meta:
        model = DayJournal


