from rest_framework import serializers
from models import Account
from core.serializers import TagSerializer


class AccountSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Account
        # exclude = ['code', 'company', 'parent', 'current_balance']
        fields = ['id', 'name', 'tags', 'current_balance']
