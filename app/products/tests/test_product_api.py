"""
Test products API
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from products.serializers import ProductSerializer

PRODUCTS_URL = reverse('products:products-list')


class ProductAPITests(TestCase):
    """Test products API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_products(self):
        """Test retrieving a list of products"""
        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

