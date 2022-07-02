"""
Database models
"""
from django.db import models

class Product(models.Model):
    """Product object"""
    models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
