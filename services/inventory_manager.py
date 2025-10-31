# ims/services/inventory_manager.py

from utils.logging_config import logger

class InventoryManager:
    def __init__(self):
        # Dictionary to store products
        # Key = product_id, Value = Product object
        self.products = {}
        
        # For storing order history later
        self.orders = []

        self.suppliers = {}


    def add_product(self, product):
        self.products[product.product_id] = product
        logger.info(f"Product added to inventory: {product.product_id}")

    def get_product(self, product_id):
        """Returns the product object if found, else None."""
        return self.products.get(product_id)

    def place_order(self, order):
        logger.info(f"Processing Order {order.order_id} ({order.order_type})")

        product = self.get_product(order.product_id)

        if product is None:
            logger.error(f"Order failed - Product {order.product_id} not found.")
            raise ValueError("Product not found in inventory")

        try:
            if order.order_type == "purchase":
                product.add_stock(order.quantity)
            elif order.order_type == "sale":
                product.reduce_stock(order.quantity)
            else:
                raise ValueError("Invalid order type")

            self.orders.append(order)
            logger.info(f"Order {order.order_id} completed successfully")

        except Exception as e:
            logger.error(f"Order {order.order_id} failed: {str(e)}")
            raise

    def add_supplier(self, supplier):
        self.suppliers[supplier.supplier_id] = supplier
        logger.info(f"Supplier added to system: {supplier.supplier_id}")

