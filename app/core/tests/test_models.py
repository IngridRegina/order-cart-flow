"""
Tests for models
"""
from decimal import Decimal

from django.test import TestCase

from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_order(self):
        """Test creating an order is successful"""
        order = models.Order.objects.create()

        self.assertEqual(str(order), order.id)
