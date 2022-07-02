"""
URL mappings for the products app
"""
from django.urls import (
    path,
    include,
)

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductView.as_view(), name='products'),
]
