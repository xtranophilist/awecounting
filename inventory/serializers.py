from rest_framework import serializers
from models import Item
from ledger.models import Account
from tax.serializers import TaxSchemeSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class ItemSerializer(serializers.ModelSerializer):
    purchase_account = AccountSerializer()
    purchase_tax_scheme = TaxSchemeSerializer()
    sales_account = AccountSerializer()
    sales_tax_scheme = TaxSchemeSerializer()
    
    class Meta:
        model = Item
