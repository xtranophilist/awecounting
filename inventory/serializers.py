from rest_framework import serializers
from models import Item, InventoryAccount
from tax.serializers import TaxSchemeSerializer
from ledger.serializers import AccountSerializer
from datetime import date


class ItemSerializer(serializers.ModelSerializer):
    purchase_account = AccountSerializer()
    purchase_tax_scheme = TaxSchemeSerializer()
    sales_account = AccountSerializer()
    sales_tax_scheme = TaxSchemeSerializer()
    
    class Meta:
        model = Item


class InventoryAccountSerializer(serializers.ModelSerializer):
    opening = serializers.SerializerMethodField('get_last_day_closing')
    # rate = serializers.SerializerMethodField('get_rate')
    rate = serializers.Field(source='item.sales_price')

    class Meta:
        model = InventoryAccount
        fields = ['id', 'name', 'opening', 'rate']

    def __init__(self, *args, **kwargs):
        day = kwargs.pop('day', None)
        super(InventoryAccountSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        transaction = obj.get_last_transaction_before(self.day)
        if transaction:
            return transaction.current_quantity

    # def get_rate(self, obj):
    #     item = obj.item
    #
    #     if transaction:
    #         return transaction.current_quantity

