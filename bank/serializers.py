from rest_framework import serializers
from bank.models import ChequeDeposit, ChequeDepositRow, ChequePayment


class ChequeDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeDepositRow


class ChequeDepositSerializer(serializers.ModelSerializer):
    rows = ChequeDepositRowSerializer()

    class Meta:
        model = ChequeDeposit


class ChequePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequePayment