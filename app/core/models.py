"""
Database models
"""
import uuid

from django.db import models


def default_amount():
    """Default amount object"""
    return {
        "discount": "0.00",
        "paid": "0.00",
        "returns": "0.00",
        "total": "0.00"
    }


class Product(models.Model):
    """Product object"""
    models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=20)


class Order(models.Model):
    """Order object"""
    ORDER_STATUS_CHOICES = [
        ('NEW', 'new'),
        ('PAID', 'paid')
    ]
    amount = models.JSONField(default=default_amount(), blank=False, null=False)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    products = list()
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='NEW')

    def __str__(self):
        return str(self.id)


class OrderProduct(models.Model):
    """Order product object"""
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False, blank=False, default=1)
    replaced_with = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='product_replaced_with'
    )
