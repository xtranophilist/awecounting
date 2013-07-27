from rest_framework import serializers
from voucher.models import SalesVoucher
from voucher.models import Particular


class ParticularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Particular


class SalesVoucherSerializer(serializers.ModelSerializer):
    particulars = ParticularSerializer()
    
    class Meta:
        model = SalesVoucher
