from rest_framework import serializers
from models import Account
from core.serializers import TagSerializer
from datetime import date


class AccountSerializer(serializers.ModelSerializer):
    categories = serializers.Field(source='all_categories')
    opening = serializers.SerializerMethodField('get_last_day_closing')

    class Meta:
        model = Account
        # exclude = ['code', 'company', 'parent', 'current_balance']
        fields = ['id', 'name', 'categories', 'opening']

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

