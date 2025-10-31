# ims/models/product.py
from utils.logging_config import logger

class Product:
    def __init__(self, product_id, name, category, price, quantity, supplier_id):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.supplier_id = supplier_id

        logger.info(f"Created Product: {name} (ID: {product_id})")

    def add_stock(self, amount):
        self.quantity += amount
        logger.info(f"Stock increased for {self.product_id} by {amount}")

    def reduce_stock(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount
            logger.info(f"Stock reduced for {self.product_id} by {amount}")
        else:
            logger.warning(f"Attempted stock reduction failed for {self.product_id} - Not enough stock")
            raise ValueError("Insufficient Stock")
