# Introduction

The project uses Django(Python) with Django REST Framework + flake8 for linting 

# Project setup

* make sure you have Docker Desktop installed and running
* in a terminal, navigate to the project root folder and run `docker-compose build`
* in the same location, run `docker-compose up`
* everything should be running, you can visit the swagger documentation page at http://localhost:8000/api/docs

# API General Description

API implements a very simple e-commerce cart/order flow:

It has a list of products;
Products can be added to the order;
Products can be modified within the order;
Products can be replaced when being assembled by the warehouse worker.

# API Endpoints
- GET /api/products - list of all available products

`curl http://localhost:8000/api/products`

- POST /api/orders - create a new order

```
curl -X POST \
  http://localhost:8000/api/orders
```

- GET /api/orders/:order_id - get order details

`curl http://localhost:8000/api/orders/:order_id`

- PATCH /api/orders/:order_id - update an order

```
curl -H "Content-Type: application/json" \
  -X PATCH \
  --data '{"status": "PAID"}' \
  http://localhost:8000/api/orders/:order_id
```

- GET /api/orders/:order_id/products - get order products

`curl http://localhost:8000/api/orders/:order_id/products`

- POST /api/orders/:order_id/products - add products to the order

```
curl -H "Content-Type: application/json" \
  --data '[123]' \ 
  http://localhost:8000/api/orders/:order_id/products
```
  
- PATCH /api/orders/:order_id/products/:product_id - update product quantity

```
curl -H "Content-Type: application/json" \
  -X PATCH \
  --data '{"quantity": 33}' \
  http://localhost:8000/api/orders/:order_id/products/:product_id
```

- PATCH /api/orders/:order_id/products/:product_id - add a replacement product

```
curl -H "Content-Type: application/json" \
  -X PATCH \
  --data '{"replaced_with": {"product_id": 123, "quantity": 6}}' \
  http://localhost:8000/api/orders/:order_id/products/:product_id
```
