import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger
from db.product_db import ProductDB
from db.supplier_db import SupplierDB
from db.orders_db import OrdersDB


class InventoryManager:
    def __init__(self):
        self.product_db = ProductDB()
        self.supplier_db = SupplierDB()
        self.orders_db = OrdersDB()

    #  BUSINESS LOGIC LAYER

    def add_supplier(self, supplier):
        """Validate & add supplier."""
        existing_supplier = self.supplier_db.get_supplier_by_id(supplier.supplier_id)

        if existing_supplier:
            logger.warning(f"Supplier {supplier.supplier_id} already exists!")
            raise ValueError("Supplier already exists")

        self.supplier_db.add_supplier(supplier)
        logger.info(f"Supplier {supplier.supplier_id} added successfully")
    
    def get_supplier(self, supplier_id: str):
        """
        Returns a Supplier object if found, else None.
        """
        return self.supplier_db.get_supplier_by_id(supplier_id)
    
    def get_all_suppliers(self):
        """Fetch all suppliers from DB."""
        suppliers = self.supplier_db.get_all_suppliers()
        logger.info(f"Fetched {len(suppliers)} suppliers from DB")
        return suppliers
   
    def remove_supplier(self, supplier_id):
        # Business rule: Check if supplier has active products
        active_products = self.product_db.get_active_products_by_supplier(supplier_id)
        if active_products:
            raise Exception("Cannot delete supplier with active products. Delete or deactivate those products first.")
        
        # Business action: soft delete the supplier
        self.supplier_db.soft_delete_supplier(supplier_id)
        
        return {"message": "Supplier deleted successfully."}

    def add_product(self, product):
        """Validate & add product."""
        existing_product = self.product_db.get_product_by_id(product.product_id)

        if existing_product:
            logger.warning(f"Product {product.product_id} already exists!")
            raise ValueError("Product already exists")

        self.product_db.add_product(product)
        logger.info(f"Product {product.product_id} added successfully")

    # Order Handling (Main Business Logic)
    def place_order(self, order):
        product = self.product_db.get_product_by_id(order.product_id)

        if not product:
            raise ValueError("Product not found")

        # Business rules:
        if order.order_type == "purchase":
            new_quantity = product.quantity + order.quantity

        elif order.order_type == "sale":
            if order.quantity > product.quantity:
                raise ValueError("Not enough stock")
            new_quantity = product.quantity - order.quantity

        else:
            raise ValueError("Invalid order type")

        #  Step 1: Update Product Stock
        self.product_db.update_stock(order.product_id, new_quantity)

        #  Step 2: Save order
        self.orders_db.add_order(order)

        logger.info(f"Order processed: {order.order_id}")

    def cancel_order(self, order_id):
        # 1. Validate
        row = self.orders_db.get_order_by_id(order_id)
        if not row:
            raise ValueError("Order not found")

        # 2. Apply business rule (soft cancel)
        self.orders_db.cancel_order(order_id)

        # 3. Return message for routes
        return {"message": "Order cancelled successfully"}

    def get_order(self, order_id: str):
        """Get a specific order by ID."""
        order = self.orders_db.get_order_by_id(order_id)
        if not order:
            logger.warning(f"Order {order_id} not found")
        return order

    def get_all_orders(self):
        """Fetch all orders."""
        orders = self.orders_db.get_all_orders()
        logger.info(f"Fetched {len(orders)} orders from DB")
        return orders

    def remove_order(self, order_id: str):
        """Delete an order by ID."""
        deleted = self.orders_db.delete_order(order_id)
        if not deleted:
            logger.warning(f"Order {order_id} not found for deletion")
            raise ValueError("Order not found")
        logger.info(f"Order {order_id} deleted successfully")
        return True

    def update_stock(self, product_id, quantity_change):
        """Update product quantity in DB."""
        product = self.product_db.get_product_by_id(product_id)

        if not product:
            raise ValueError(f"Product {product_id} does not exist")

        # Business rule: Avoid negative stock
        if product.quantity + quantity_change < 0:
            raise ValueError("Insufficient stock")

        new_quantity = product.quantity + quantity_change
        self.product_db.update_stock(product_id, new_quantity)

        logger.info(
            f"Stock updated for {product_id}. Change: {quantity_change}, New Qty: {new_quantity}"
        )

    def get_product(self, product_id: str):
        product = self.product_db.get_product_by_id(product_id)
        return product
    
    def remove_product(self, product_id):
        """Soft delete a product by marking it as deleted."""
        try:
            # Check if product exists
            row = self.product_db.fetch_one(
                "SELECT * FROM products WHERE product_id = ?", (product_id,)
            )
            if not row:
                raise Exception(f"Product {product_id} not found.")

            # Soft delete
            self.product_db.execute_query(
                "UPDATE products SET is_deleted = 1 WHERE product_id = ?", (product_id,)
            )

            logger.info(f"Product {product_id} marked as deleted.")
            return {"message": "Product deleted successfully."}

        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            raise

    def get_inventory(self):
        """Fetch all products from DB."""
        return self.product_db.get_all_products()
    
    def get_order_history(self):
        return self.orders_db.get_all_orders()
