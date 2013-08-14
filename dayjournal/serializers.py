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
    account_id = serializers.Field(source='purchase_ledger_id')

    class Meta:
        model = CashPurchase
        exclude = ['day_journal', 'purchase_ledger']


class CashReceiptSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='received_from_id')

    class Meta:
        model = CashReceipt
        exclude = ['day_journal', 'received_from']


class CashPaymentSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='payment_to_id')

    class Meta:
        model = CashPayment
        exclude = ['day_journal', 'payment_to']


class CreditSalesSerializer(serializers.ModelSerializer):
    account_cr_id = serializers.Field(source='sales_ledger_id')
    account_dr_id = serializers.Field(source='customer_id')

    class Meta:
        model = CreditSales
        exclude = ['day_journal', 'sales_ledger', 'customer']


class CreditPurchaseSerializer(serializers.ModelSerializer):
    account_dr_id = serializers.Field(source='purchase_ledger_id')
    account_cr_id = serializers.Field(source='supplier_id')

    class Meta:
        model = CreditPurchase
        exclude = ['day_journal', 'purchase_ledger', 'supplier']


class CreditExpenseSerializer(serializers.ModelSerializer):
    account_cr_id = serializers.Field(source='expense_head')
    account_dr_id = serializers.Field(source='expense_claimed_by_id')

    class Meta:
        model = CreditExpense
        exclude = ['day_journal', 'expense_head', 'expense_claimed_by']


class CreditIncomeSerializer(serializers.ModelSerializer):
    account_dr_id = serializers.Field(source='income_head_id')
    account_cr_id = serializers.Field(source='income_from_id')

    class Meta:
        model = CreditIncome
        exclude = ['day_journal', 'income_head', 'income_from']


class SummaryCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryCash
        exclude = ['day_journal']


class SummaryEquivalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryEquivalent
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    # cash_sales = CashSalesSerializer()
    # cash_purchase = CashPurchaseSerializer()
    # cash_receipt = CashReceiptSerializer()
    # cash_payment = CashPaymentSerializer()
    # credit_sales = CreditSalesSerializer()
    # credit_purchase = CreditPurchaseSerializer()
    # credit_expense = CreditExpenseSerializer()
    # credit_income = CreditIncomeSerializer()
    summary_cash = SummaryCashSerializer()
    summary_equivalent = SummaryEquivalentSerializer()

    class Meta:
        model = DayJournal
        exclude = ['company']
