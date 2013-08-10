from rest_framework import serializers
from voucher.models import Invoice, PurchaseVoucher
from voucher.models import Particular


class ParticularSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = Particular
        exclude = ['item']


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    particulars = ParticularSerializer()
    
    class Meta:
        model = Invoice
        exclude = ['company']


class PurchaseVoucherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = PurchaseVoucher
