from rest_framework import serializers
from journal.models import DayJournal, DayCashSales, DayCashPurchase, DayCashReceipt, DayCashPayment, DaySummaryCash, \
    DaySummaryBank, DaySummaryEquivalent, DaySummarySalesTax, DaySummaryInventory, DayCreditExpense, DayCreditIncome, \
    DayCreditPurchase, DayCreditSales, DayPayroll


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


class DaySummaryCashSerializer(serializers.ModelSerializer):

    class Meta:
        model = DaySummaryCash
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    day_cash_sales = DayCashSalesSerializer()
    day_cash_purchase = DayCashPurchaseSerializer()
    day_cash_receipt = DayCashReceiptSerializer()
    day_cash_payment = DayCashPaymentSerializer()
    day_summary_cash = DaySummaryCashSerializer()

    class Meta:
        model = DayJournal
        exclude = ['company']


