from rest_framework import serializers
from journal.models import DayJournal, DayCashSales, DayCashPurchase, DayCashReceipt, DayCashPayment


class DayCashSalesSerializer(serializers.ModelSerializer):
    # item = serializers.Field(source='item.name')
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = DayCashSales
        exclude = ['day_journal', 'item']


class DayCashPurchaseSerializer(serializers.ModelSerializer):
    item = serializers.Field(source='item.name')
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = DayCashPurchase
        exclude = ['day_journal']


class DayCashReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayCashReceipt
        exclude = ['day_journal']


class DayCashPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayCashPayment
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    day_cash_sales = DayCashSalesSerializer()
    day_cash_purchase = DayCashPurchaseSerializer()
    day_cash_receipt = DayCashReceiptSerializer()
    day_cash_payment = DayCashPaymentSerializer()

    class Meta:
        model = DayJournal
        exclude = ['company']


