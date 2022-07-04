"""
Tests for models
"""

from core import models
from django.test import TestCase


class ModelTests(TestCase):
    """Test models"""

    def test_create_order(self):
        """Test creating an order is successful"""
        order = models.Order.objects.create()

        self.assertEqual(str(order), str(order.id))
