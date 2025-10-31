# ims/models/order.py
from utils.logging_config import logger
from datetime import datetime

class Order:
    def __init__(self, order_id, product_id, quantity, order_type, date=None):
        """
        Represents a purchase or sales order.
        
        Args:
            order_id (str): Unique ID for the order
            product_id (str): ID of the product involved in this order
            quantity (int): Quantity of product purchased or sold
            order_type (str): "purchase" or "sale"
            date (str or datetime, optional): Order date, defaults to today's date
        """
        
        if quantity <= 0:
            logger.error(f"Invalid quantity for Order {order_id}: {quantity}")
            raise ValueError("Quantity must be greater than zero")

        if order_type not in ["purchase", "sale"]:
            logger.error(f"Invalid order type for {order_id}: {order_type}")
            raise ValueError("Order type must be 'purchase' or 'sale'")
        
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_type = order_type
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"Created Order: ID={order_id}, Type={order_type}, Product={product_id}, Qty={quantity}")

    def __repr__(self):
        return f"<Order: {self.order_id}, {self.order_type}, Qty: {self.quantity}>"
