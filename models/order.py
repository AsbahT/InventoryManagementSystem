# ims/models/order.py
import sqlite3,os,sys
import uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger
from datetime import datetime

class Order:
    def __init__(self, product_id, order_type,quantity, date,supplier_id,order_id=None,status='active'):
        """
        Represents a purchase or sales order.
        
        Args:
            order_id (str): Unique ID for the order
            product_id (str): ID of the product involved in this order
            quantity (int): Quantity of product purchased or sold
            order_type (str): "purchase" or "sale"
            date (str or datetime, optional): Order date, defaults to today's date
        """
        self.order_id = order_id if order_id is not None else str(uuid.uuid4())
        self.product_id = product_id
        self.quantity = int(quantity)
        self.order_type = order_type.lower().strip()
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.supplier_id = supplier_id
        self.status = status

        if quantity <= 0:
            logger.error(f"Invalid quantity for Order {self}: {quantity}")
            raise ValueError("Quantity must be greater than zero")

        if self.order_type not in ["purchase", "sale"]:
            logger.error(f"Invalid order type for {self}: {order_type}")
            raise ValueError(f"Order type must be 'purchase' or 'sale', got '{order_type}'")
            

        logger.info(f"Created Order: {self}, Type={order_type}, Product={product_id}, Qty={quantity}")

    def __repr__(self):
        return f"<Order: {self.order_id}, {self.order_type}, Qty: {self.quantity}>"
