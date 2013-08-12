from rest_framework import serializers
from daybook.models import DayBook, CashSales, CashPurchase, CashReceipt, CashPayment, SummaryCash, \
    SummaryBank, SummaryEquivalent, SummarySalesTax, SummaryInventory, CreditExpense, CreditIncome, \
    CreditPurchase, CreditSales


class CashSalesSerializer(serializers.ModelSerializer):
    # item = serializers.Field(source='item.name')
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = CashSales
        exclude = ['day_book', 'item']


class CashPurchaseSerializer(serializers.ModelSerializer):
    item = serializers.Field(source='item.name')
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = CashPurchase
        exclude = ['day_book']


class CashReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashReceipt
        exclude = ['day_book']


class CashPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashPayment
        exclude = ['day_book']


class SummaryCashSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryCash
        exclude = ['day_book']


class DayBookSerializer(serializers.ModelSerializer):
    cash_sales = CashSalesSerializer()
    cash_purchase = CashPurchaseSerializer()
    cash_receipt = CashReceiptSerializer()
    cash_payment = CashPaymentSerializer()
    summary_cash = SummaryCashSerializer()

    class Meta:
        model = DayBook
        exclude = ['company']


