from rest_framework import serializers
from models import Item, InventoryAccount
from tax.serializers import TaxSchemeSerializer
from ledger.serializers import AccountSerializer


class ItemSerializer(serializers.ModelSerializer):
    purchase_account = AccountSerializer()
    purchase_tax_scheme = TaxSchemeSerializer()
    sales_account = AccountSerializer()
    sales_tax_scheme = TaxSchemeSerializer()
    
    class Meta:
        model = Item


class InventoryAccountSerializer(serializers.ModelSerializer):
    current_amount = serializers.Field('transactions.0')

    class Meta:
        model = InventoryAccount
        exclude = ['company', 'code']