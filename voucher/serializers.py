from rest_framework import serializers
from voucher.models import SalesVoucher

class SalesVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesVoucher
