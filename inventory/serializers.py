from rest_framework import serializers
from models import Item
from ledger.models import Account
from tax.models import TaxScheme


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class TaxSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxScheme
        exclude = ['company']


class ItemSerializer(serializers.ModelSerializer):
    purchase_account = AccountSerializer()
    purchase_tax_scheme = TaxSchemeSerializer()
    sales_account = AccountSerializer()
    sales_tax_scheme = TaxSchemeSerializer()
    
    class Meta:
        model = Item
