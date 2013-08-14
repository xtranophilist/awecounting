from rest_framework import serializers
from models import Account, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class AccountSerializer(serializers.ModelSerializer):
    tags = serializers.RelatedField(many=True)

    class Meta:
        model = Account
        # exclude = ['code', 'company', 'parent', 'current_balance']
        fields = ['id', 'name', 'tags', 'current_balance']
