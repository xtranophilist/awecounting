from rest_framework import serializers
from core.models import Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
