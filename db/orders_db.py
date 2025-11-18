import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger
from models.order import Order
from db.database import Database

class OrdersDB(Database):

    def __init__(self):
        super().__init__()
        self.execute_query("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    order_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    supplier_id TEXT,  
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                );
            """,)



    def add_order(self, order:Order):
        try:
            self.execute_query(
                "INSERT INTO orders (product_id, order_type, quantity, date, supplier_id) VALUES (?, ?, ?, ?, ?)",
                (order.product_id, order.order_type, order.quantity, order.date, order.supplier_id),
            )
            logger.info(f"Order saved in DB: {order.order_id}")
            logger.debug(f"Order being added: {order}")


        except Exception as e:
            logger.error(f"Error saving order {order.order_id}: {e}")
            raise

    def get_order_by_id(self, order_id):
        """Fetch single order"""
        result = self.fetch_one(
            "SELECT * FROM orders WHERE order_id = ?",
            (order_id,)
        )

        if result:
            return Order(**dict(result))
        return None

    def get_all_orders(self):
        """Fetch all orders"""
        rows = self.fetch_all("SELECT * FROM orders WHERE status = 'active' ORDER BY order_id")
        # return [Order(**dict(row)) for row in rows]
        return [
        Order(
            order_id=row['order_id'],
            product_id=row['product_id'],
            order_type=row['order_type'],
            quantity=row['quantity'],
            date=row['date'],
            supplier_id=row['supplier_id']
        )
        for row in rows
    ]

    def get_orders_by_product(self, product_id):
        """Fetch orders for a specific product"""
        rows = self.fetch_all(
            "SELECT * FROM orders WHERE product_id = ?",
            (product_id,)
        )
        return [Order(**dict(row)) for row in rows]

    def cancel_order(self, order_id):
        return self.execute_query(
            "UPDATE orders SET status = 'cancelled' WHERE order_id = ?", (order_id,)
        )

if __name__ == "__main__":
    db_order = OrdersDB()
    print("OrdersDB instance created successfully!")