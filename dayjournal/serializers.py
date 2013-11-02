from rest_framework import serializers
from dayjournal.models import DayJournal, CashSales, SummaryInventory, CashEquivalentSales, \
    SummaryTransfer, CardSales, LottoDetail, InventoryFuel


class CashSalesSerializer(serializers.ModelSerializer):
    account_id = serializers.Field(source='sales_ledger_id')

    class Meta:
        model = CashSales
        exclude = ['day_journal', 'sales_ledger']


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


class LottoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LottoDetail
        exclude = ['day_journal']


class DayJournalSerializer(serializers.ModelSerializer):
    cash_sales = CashSalesSerializer()
    summary_transfer = SummaryTransferSerializer()
    summary_inventory = SummaryInventorySerializer()
    card_sales = CardSalesSerializer()
    cash_equivalent_sales = CashEquivalentSalesSerializer()
    lotto_detail = LottoDetailSerializer()
    inventory_fuel = InventoryFuelSerializer()

    class Meta:
        model = DayJournal
        exclude = ['company']