from rest_framework import serializers
from voucher.models import Invoice, PurchaseVoucher
from voucher.models import InvoiceParticular, PurchaseParticular


class InvoiceParticularSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = InvoiceParticular
        exclude = ['item']


class PurchaseParticularSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = PurchaseParticular
        exclude = ['item']


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    particulars = InvoiceParticularSerializer()
    
    class Meta:
        model = Invoice
        exclude = ['company']


class PurchaseVoucherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    particulars = PurchaseParticularSerializer()

    class Meta:
        model = PurchaseVoucher
