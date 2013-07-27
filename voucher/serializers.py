from rest_framework import serializers
from voucher.models import Invoice
from voucher.models import Particular


class ParticularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Particular


class InvoiceSerializer(serializers.ModelSerializer):
    particulars = ParticularSerializer()
    
    class Meta:
        model = Invoice
