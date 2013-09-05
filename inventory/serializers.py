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
    rate = serializers.SerializerMethodField('get_rate')

    class Meta:
        model = InventoryAccount
        fields = ['id', 'name', 'rate', 'opening']

    def __init__(self, *args, **kwargs):
        day = kwargs.pop('day', None)
        super(InventoryAccountSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        return obj.get_day_opening(self.day)

    def get_rate(self, obj):
        try:
            return obj.item.sales_price
        except:
            return None
