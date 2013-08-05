from rest_framework import serializers
from journal.models import DayJournal, DayCashSales


class DayCashSalesSerializer(serializers.ModelSerializer):
    item = serializers.Field(source='item.name')
    item_id = serializers.Field(source='item_id')
    class Meta:
        model = DayCashSales



class DayJournalSerializer(serializers.ModelSerializer):
    day_cash_sales = DayCashSalesSerializer()
    # daycashpurchase_set
    # day_cash_purchase = models.ManyToManyField(DayCashPurchase)
    # day_cash_receipt = models.ManyToManyField(DayCashReceipt)
    # day_cash_payment = models.ManyToManyField(DayCashPayment)
    # day_credit_sales = models.ManyToManyField(DayCreditSales)
    # day_credit_purchase = models.ManyToManyField(DayCreditPurchase)
    # day_credit_expense = models.ManyToManyField(DayCreditExpense)
    # day_credit_income = models.ManyToManyField(DayCreditIncome)
    # day_summary_equivalent = models.ManyToManyField(DaySummaryEquivalent)
    # day_summary_bank = models.ManyToManyField(DaySummaryBank)
    # day_summary_sales_tax = models.ManyToManyField(DaySummarySalesTax)
    # day_summary_inventory = models.ManyToManyField(DaySummaryInventory)
    # day_payroll = models.ManyToManyField(DayPayroll)
    # day_summary_cash

    class Meta:
        model = DayJournal
        # depth = 1


