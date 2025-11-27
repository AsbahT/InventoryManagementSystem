# 📦 Inventory, Product & Order Management API (FastAPI)

A modular **Inventory Management System** built using **FastAPI**, providing APIs for managing **Products**, **Suppliers**, and **Orders** with clean separation between models, services, and routers.

This project is ideal for learning API design, inventory workflows, and scalable backend structuring.

---

# ✨ Features

### 🛍 **Products**

* Add new products
* View all products
* View product details
* Update stock quantity
* Link product to supplier

### 🏭 **Suppliers**

* Register suppliers
* View all suppliers
* Get supplier details
* Manage supplier–product relationships

### 📦 **Orders**

* Place orders
* Validate product stock
* Deduct/restore inventory
* Fetch order history
* Cancel orders

### 📊 **Inventory Manager**

* Central logic for stock updates
* Manages product availability
* Stores order history
* Links orders with products

---

# 📁 Project Structure

```
project/
│── app/
│   ├── models/
│   │   ├── order.py
│   │   ├── product.py
│   │   └── supplier.py
│   ├── services/
│   │   ├── inventory_manager.py
│   ├── routes/
│   │   ├── orders_api.py
│   │   ├── products_api.py
│   │   └── suppliers_api.py
|   |__db/
│   │   ├── orders_db.py
│   │   ├── products_db.py
│   │   └── suppliers_db.py
│   │   ├── database.py
│   │   ├── setup_db.py
│   │   └── ims.db
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

# 🧩 Core Components Overview

## 🛍 **Products**

A product typically looks like:

```json
{
  "product_id": "A1",
  "name": "Laptop Charger",
  "category":"Electronics",
  "price": 25.00,
  "quantity": 50,
  "supplier_id": "S100",
  
}
```

Products are:

* created via Inventory Manager
* linked to suppliers
* have stock updated when orders are processed

---

## 🏭 **Suppliers**

Example supplier:

```json
{
  "supplier_id": "S100",
  "name": "TechSupply Co.",
  "contact_info": "contact@techsupply.com"
}
```

Suppliers:

* can supply multiple products
* are stored and managed separately
* are referenced by product objects

---

## 📦 **Orders**

Example order:

```json
{
  "order_id": "O101",
  "product_id":"P001",
  "order_type":"Sale",
  "quantity":20,
  "date":"26-10-2024",
  "supplier_id":"S001"
}
```

Order pipeline:

1. Validate product stock
2. Deduct inventory
3. Save order
4. Cancel → restore stock

---

## 🔧 **Inventory Manager**

Responsible for:

* stock updates
* checking availability
* tracking order history
* linking orders and products

Key methods typically include:

* `place_order(order)`
* `cancel_order(order_id)`
* `get_order_history()`
* `get_order(order_id)`

---

# 🛠 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Application

Start the FastAPI server:

```bash
uvicorn api:api.api_main --reload
```

The API will be available at:

* Swagger UI → **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
---

# 📌 API Endpoints Documentation

---

# 🛍 **Products API**

### ➤ **POST /products/**

Create a new product.

### ➤ **GET /products/**

List all products.

### ➤ **GET /products/{product_id}**

Get a product by product_id.

---

# 🏭 **Suppliers API**

### ➤ **POST /suppliers/**

Create a new supplier.

### ➤ **GET /suppliers/**

List all suppliers.

### ➤ **GET /suppliers/{supplier_id}**

Get a supplier by supplier_id.

---

# 📦 **Orders API**

### ➤ **POST /orders/**

Place a new order.

### ➤ **GET /orders/**

List all orders.

### ➤ **GET /orders/{order_id}**

Get details of a specific order.

### ➤ **DELETE /orders/{order_id}**

Cancel an order and restore product stock.

---

# 🧰 Technologies Used

* **Python 3.10+**
* **FastAPI**
* **Pydantic**
* **Uvicorn**
* **Modular architecture (Models, Routers, Services)**

---

# 🚀 Future Enhancements

* Add authentication (JWT)
* Add order invoice generation
* Add supplier performance analytics
* Add category support for products
* Low-stock alerts

---

# 📄 License

This project is open-source. 
