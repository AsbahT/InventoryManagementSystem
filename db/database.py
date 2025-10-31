# ims/db/database.py

import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger

DB_NAME = "ims.db"

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()
        logger.info("Connected to SQLite database")
        self.create_tables()

    def create_tables(self):
        try:
            # Create Suppliers Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    supplier_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact TEXT
                );
            """)

            # Create Products Table
            self.cursor.execute("""
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

            # Create Orders Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    order_type TEXT CHECK(order_type IN ('purchase', 'sale')),
                    date TEXT NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                );
            """)

            self.connection.commit()
            logger.info("Database tables created successfully")

        except Exception as e:
            logger.error(f"Error creating tables: {e}")

    def close(self):
        self.connection.close()
        logger.info("Database connection closed")
