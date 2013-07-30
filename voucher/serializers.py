from rest_framework import serializers
from voucher.models import Invoice, PurchaseVoucher
from voucher.models import Particular


class ParticularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Particular


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    particulars = ParticularSerializer()
    
    class Meta:
        model = Invoice


class PurchaseVoucherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = PurchaseVoucher
