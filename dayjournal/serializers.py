from rest_framework import serializers
from dayjournal.models import DayJournal, CashSales, CashPurchase, CashReceipt, CashPayment, \
    SummaryInventory, CreditExpense, CreditIncome, CreditPurchase, CashEquivalentSales, \
    CreditSales, SummaryLotto, SummaryTransfer, CardSales, ChequePurchase, LottoDetail, InventoryFuel


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


class SummaryLottoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryLotto
        exclude = ['day_journal']


class SummaryTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryTransfer
        exclude = ['day_journal']


class SummaryInventorySerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='particular_id')

    class Meta:
        model = SummaryInventory
        exclude = ['day_journal', 'particular']


class InventoryFuelSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='particular_id')

    class Meta:
        model = InventoryFuel
        exclude = ['day_journal', 'particular']


class CardSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardSales
        exclude = ['day_journal']


class CashEquivalentSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashEquivalentSales
        exclude = ['day_journal']


class ChequePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequePurchase
        exclude = ['day_journal']


class LottoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LottoDetail
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    cash_sales = CashSalesSerializer()
    cash_purchase = CashPurchaseSerializer()
    cash_receipt = CashReceiptSerializer()
    cash_payment = CashPaymentSerializer()
    credit_sales = CreditSalesSerializer()
    credit_purchase = CreditPurchaseSerializer()
    credit_expense = CreditExpenseSerializer()
    credit_income = CreditIncomeSerializer()
    summary_lotto = SummaryLottoSerializer()
    summary_transfer = SummaryTransferSerializer()
    summary_inventory = SummaryInventorySerializer()
    card_sales = CardSalesSerializer()
    cash_equivalent_sales = CashEquivalentSalesSerializer()
    cheque_purchase = ChequePurchaseSerializer()
    lotto_detail = LottoDetailSerializer()

    class Meta:
        model = DayJournal
        exclude = ['company']