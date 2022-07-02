"""
Serializers for products API
"""
from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']
