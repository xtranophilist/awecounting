from datetime import date

from rest_framework import serializers

from models import Account, Party


class AccountSerializer(serializers.ModelSerializer):
    opening = serializers.SerializerMethodField('get_last_day_closing')
    # opening = serializers.Field(source='day_opening')
    categories = serializers.Field()

    class Meta:
        model = Account
        # exclude = ['code', 'company', 'parent', 'current_balance']
        fields = ['id', 'name', 'categories', 'opening', 'tax_rate']
        # fields = ['id', 'name', 'categories', 'tax_rate']

    def __init__(self, *args, **kwargs):

        day = kwargs.pop('day', None)
        super(AccountSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        return obj.get_day_opening(self.day)


class PartySerializer(serializers.ModelSerializer):
    customer_balance = serializers.Field(source='customer_account.get_balance')
    supplier_balance = serializers.Field(source='supplier_account.get_balance')
    class Meta:
        model = Party