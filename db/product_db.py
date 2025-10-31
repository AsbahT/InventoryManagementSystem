# ims/db/product_db.py
import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger
from models.product import Product

DB_NAME = "ims.db"

class ProductDB:
    
    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    def add_product(self, product: Product):
        try:
            self.cursor.execute("""
                INSERT INTO products (product_id, name, category, price, quantity, supplier_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (product.product_id, product.name, product.category,
                  product.price, product.quantity, product.supplier_id))
            
            self.connection.commit()
            logger.info(f"Product saved to DB: {product.product_id}")
        except Exception as e:
            logger.error(f"Failed to add product: {e}")

    def get_product(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        row = self.cursor.fetchone()

        if row:
            return Product(*row)
        return None

    def update_stock(self, product_id, new_quantity):
        try:
            self.cursor.execute("""
                UPDATE products SET quantity = ? WHERE product_id = ?
            """, (new_quantity, product_id))
            self.connection.commit()
            logger.info(f"Stock updated for: {product_id}")
        except Exception as e:
            logger.error(f"Failed to update stock: {e}")

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()

        return [Product(*row) for row in rows]

    def close(self):
        self.connection.close()
