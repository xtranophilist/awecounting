from rest_framework import serializers
from bank.models import ChequeReceipt, ChequeReceiptRow


class ChequeReceiptRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeReceiptRow


class ChequeReceiptSerializer(serializers.ModelSerializer):
    particulars = ChequeReceiptRowSerializer()

    class Meta:
        model = ChequeReceipt