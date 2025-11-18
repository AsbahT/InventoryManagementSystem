# ims/db/product_db.py
import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger
from models.product import Product
from db.database import Database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ims.db")

class ProductDB(Database):
    
    def __init__(self):
        super().__init__()
        print("creating Product table")
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    supplier_id TEXT,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            );
        """)
      

    def add_product(self, product: Product):
        try:
            self.execute_query("""
                INSERT INTO products (product_id, name, category, price, quantity, supplier_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (product.product_id, product.name, product.category,
                  product.price, product.quantity, product.supplier_id))
            
            # self.connection.commit()
            logger.info(f"Product saved to DB: {product.product_id}")
        except Exception as e:
            logger.error(f"Failed to add product: {e}")

    def get_product_by_id(self, product_id: str):
        row = self.fetch_one("SELECT * FROM products WHERE product_id = ?", (product_id,))
        return Product(**row) if row else None

    def update_stock(self, product_id, new_quantity):
        try:
            self.execute_query("""
                UPDATE products SET quantity = ? WHERE product_id = ?
            """, (new_quantity, product_id))
            logger.info(f"Stock updated for: {product_id}")
        except Exception as e:
            logger.error(f"Failed to update stock: {e}")

    def get_all_products(self):
        rows = self.fetch_all("SELECT * FROM products WHERE is_deleted = 0 ORDER BY product_id")
        return [Product(**row) for row in rows]
    
    def get_active_products_by_supplier(self, supplier_id):
        """Return a list of active (not deleted) products for a supplier."""
        return self.fetch_all(
            "SELECT * FROM products WHERE supplier_id = ? AND is_deleted = 0",
            (supplier_id,)
        )


if __name__ == "__main__":
    db_product = ProductDB()  # This will trigger __init__ and create the table
    print("ProductDB instance created successfully!")
