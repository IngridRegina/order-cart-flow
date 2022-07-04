"""
URL mappings for the orders app
"""
from django.urls import (
    path
)

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.CreateOrderView.as_view(), name='create'),
    path('<uuid:order_id>', views.OrderView.as_view(), name='order'),
    path('<uuid:order_id>/products', views.OrderProductsView.as_view(), name='products'),
    path('<uuid:order_id>/products/<uuid:product_id>', views.OrderProductDetailView.as_view(), name='product')
]
