from rest_framework import serializers
from dayjournal.models import DayJournal, CashSales, CashPurchase, CashReceipt, CashPayment, SummaryCash, \
    SummaryBank, SummaryEquivalent, SummarySalesTax, SummaryInventory, CreditExpense, CreditIncome, \
    CreditPurchase, CreditSales


class CashSalesSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='sales_ledger_id')

    class Meta:
        model = CashSales
        exclude = ['day_journal', 'sales_ledger']


class CashPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashPurchase
        exclude = ['day_journal']


class CashReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashReceipt
        exclude = ['day_journal']


class CashPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashPayment
        exclude = ['day_journal']


class SummaryCashSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryCash
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    cash_sales = CashSalesSerializer()
    cash_purchase = CashPurchaseSerializer()
    cash_receipt = CashReceiptSerializer()
    cash_payment = CashPaymentSerializer()
    summary_cash = SummaryCashSerializer()

    class Meta:
        model = DayJournal
        exclude = ['company']


