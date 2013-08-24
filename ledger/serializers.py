from rest_framework import serializers
from models import Account
from core.serializers import CategorySerializer
from datetime import date


class AccountSerializer(serializers.ModelSerializer):
    opening = serializers.SerializerMethodField('get_last_day_closing')
    # opening = serializers.Field(source='day_opening')
    categories = serializers.Field()

    class Meta:
        model = Account
        # exclude = ['code', 'company', 'parent', 'current_balance']
        fields = ['id', 'name', 'categories', 'opening', 'tax_rate']

    def __init__(self, *args, **kwargs):
        day = kwargs.pop('day', None)
        super(AccountSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        transaction = obj.get_last_transaction_before(self.day)
        if transaction:
            return transaction.current_balance

