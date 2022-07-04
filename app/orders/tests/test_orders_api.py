"""
Test orders API
"""
from core.models import Order
from django.test import TestCase
from django.urls import reverse
from orders.serializers import OrderSerializer
from rest_framework import status
from rest_framework.test import APIClient

ORDERS_URL = reverse('orders:order-list')


def detail_url(order_id):
    """Create and return an order detail URL"""
    return reverse('orders:order-detail', args=[order_id])


def products_url(order_id):
    """Create and return order products URL"""
    return reverse('orders:order-products', args=[order_id])


def product_url(order_id, product_id):
    """Create and return order single product URL"""
    return reverse('orders:order-product', args=[order_id, product_id])


def create_order():
    """Create and return a sample order"""
    order = Order.objects.create()
    return order


class OrdersAPITests(TestCase):
    """Test orders API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_create_new_order(self):
        res = self.client.post(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.object.get(id=res.data['id'])
        self.assertEqual(order.status, "NEW")

    def test_get_order_details(self):
        """Test get order details"""
        order = create_order()

        url = detail_url(order.id)
        res = self.client.get(url)

        serializer = OrderSerializer(order)
        self.assertEqual(res.data, serializer.data)

    def test_update_order_valid_status(self):
        """Test updating order with valid new status"""
        order = create_order()
        payload = {'status': 'PAID'}
        url = detail_url(order.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.amount, self.amount)
        self.assertEqual(order.id, self.id)
        self.assertEqual(order.products, self.products)
        self.assertEqual(order.status, payload['status'])

    def test_update_order_invalid_status(self):
        """Test updating order with invalid status returns error"""
        order = create_order()
        payload = {'status': 'PENDING'}
        url = detail_url(order.id)
        res = self.client.patch(url, payload)
        messages = list(res.context['messages'])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()

        self.assertNotEqual(order.status, payload['status'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid order status')

    def test_update_order_no_parameters(self):
        """Test updating order without parameters returns error"""
        order = create_order()
        url = detail_url(order.id)
        res = self.client.patch(url)
        messages = list(res.context['messages'])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid parameters')

    def test_update_order_invalid_parameters(self):
        """Test updating order with invalid parameters returns error"""
        order = create_order()
        payload = {'id': 'f8a1ecd2-ee2a-438a-bb8c-e12bd45ff781'}
        url = detail_url(order.id)
        res = self.client.patch(url, payload)
        messages = list(res.context['messages'])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()

        self.assertNotEqual(order.id, payload['id'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid order status')

    def test_get_order_products(self):
        """Test get list of order products"""
        order = create_order()
        url = products_url(order.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_add_products_to_order(self):
        """Test add products to order"""
        order = create_order()
        payload = [123, 456, 999]
        url = products_url(order.id)

        post_res = self.client.post(url, payload)

        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_update_product_quantity(self):
        """Test updating product quantity"""
        order = create_order()
        add_products_payload = [456]
        update_product_payload = {'quantity': 5}
        order_products_url = products_url(order.id)

        add_products_res = self.client.post(order_products_url, add_products_payload)

        order_product_url = product_url(order.id, add_products_res.data.products[0].id)

        res = self.client.patch(order_product_url, update_product_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.products[0].quantity, update_product_payload['quantity'])

    def test_update_product_invalid_parameters(self):
        """Test updating product with invalid parameters returns error"""
        order = create_order()
        add_products_payload = [456]
        update_product_payload = {'quantity': "5"}
        order_products_url = products_url(order.id)

        add_products_res = self.client.post(order_products_url, add_products_payload)
        order_product_url = product_url(order.id, add_products_res.data.products[0].id)
        res = self.client.patch(order_product_url, update_product_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertNotEqual(order.products[0].quantity, update_product_payload['quantity'])

    def test_add_replacement_product(self):
        """Test adding a replacement product returns error"""
        order = create_order()
        add_products_payload = [456]
        replace_product_payload = {'replaced_with': {"product_id": 123, "quantity": 6}}
        order_products_url = products_url(order.id)

        add_products_res = self.client.post(order_products_url, add_products_payload)

        order_product_url = product_url(order.id, add_products_res.data.products[0].id)

        res = self.client.patch(order_product_url, replace_product_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
