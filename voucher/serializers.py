from rest_framework import serializers
from voucher.models import Invoice, PurchaseVoucher, InvoiceParticular, PurchaseParticular, JournalVoucher, \
    JournalVoucherRow, CashReceipt, CashReceiptRow


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


class JournalVoucherRowSerializer(serializers.ModelSerializer):
    account = serializers.Field(source='account_id')

    class Meta:
        model = JournalVoucherRow
        exclude = ['dr_account', 'cr_account']


class JournalVoucherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    rows = JournalVoucherRowSerializer()

    class Meta:
        model = JournalVoucher
        exclude = ['company']


class CashReceiptRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashReceiptRow


class CashReceiptSerializer(serializers.ModelSerializer):
    rows = CashReceiptRowSerializer()

    class Meta:
        model = CashReceipt


