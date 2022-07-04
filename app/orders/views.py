"""
Views for the orders API
"""

from core.models import Order
from core.models import OrderProduct
from orders import serializers
from rest_framework import (
    generics,
    exceptions
)


class CreateOrderView(generics.CreateAPIView):
    """Create a new order"""
    serializer_class = serializers.NewOrderSerializer


class OrderView(generics.RetrieveUpdateAPIView):
    """View or update order details"""
    queryset = Order.objects.all()
    serializer_class = serializers.UpdatedOrderSerializer
    http_method_names = ['get', 'patch']

    def get_object(self):
        try:
            return Order.objects.get(pk=self.kwargs['order_id'])
        except Order.DoesNotExist:
            raise exceptions.NotFound()


class OrderProductsView(generics.ListCreateAPIView):
    """View/add order products"""
    queryset = OrderProduct.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.OrderProductIdsSerializer


class OrderProductDetailView(generics.UpdateAPIView):
    """Update order product"""
    http_method_names = ['patch']
    queryset = OrderProduct.objects.all()
    serializer_class = serializers.OrderProductSerializer
    lookup_field = 'id'
