"""
Serializers for orders API
"""
from core.models import (
    Order,
    OrderProduct,
)
from rest_framework import serializers


class OrderProductSerializer(serializers.ModelSerializer):
    """Serializer for order product"""

    class Meta:
        model = OrderProduct
        fields = ['id', 'name', 'price', 'product_id', 'quantity', 'replaced_with']
        read_only_fields = ['id', 'name', 'price', 'product_id', 'quantity', 'replaced_with']


class OrderProductIdsSerializer(serializers.Serializer):
    """Serializer for product id list"""
    ids = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderProduct.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['ids']


class NewOrderSerializer(serializers.ModelSerializer):
    """Serializer for order"""

    products = OrderProductSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Order
        fields = ['amount', 'id', 'products', 'status']
        read_only_fields = ['amount', 'id', 'status']


class UpdatedOrderSerializer(serializers.ModelSerializer):
    """Serializer for order"""

    products = OrderProductSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Order
        fields = ['amount', 'id', 'products', 'status']
        read_only_fields = ['amount', 'id']
