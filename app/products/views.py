"""
Views for the products API
"""

from rest_framework import generics

from core.models import Product
from products import serializers

class ProductView(generics.ListAPIView):
    """View for products API"""
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for request"""
        return self.serializer_class

