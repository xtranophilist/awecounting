from rest_framework import serializers
from bank.models import ChequeReceipt, ChequeReceiptRow, ChequePayment


class ChequeReceiptRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeReceiptRow


class ChequeReceiptSerializer(serializers.ModelSerializer):
    rows = ChequeReceiptRowSerializer()

    class Meta:
        model = ChequeReceipt


class ChequePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequePayment