from rest_framework import serializers
from models import Item
from tax.serializers import TaxSchemeSerializer
from ledger.serializers import AccountSerializer


class ItemSerializer(serializers.ModelSerializer):
    purchase_account = AccountSerializer()
    purchase_tax_scheme = TaxSchemeSerializer()
    sales_account = AccountSerializer()
    sales_tax_scheme = TaxSchemeSerializer()
    
    class Meta:
        model = Item
