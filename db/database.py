# ims/db/database.py

import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ims.db")


class Database:
    def __init__(self):
        print("CONNECTED TO DB:", DB_NAME)
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Enable safe multi-thread writes
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA busy_timeout = 5000;")
        self.conn.execute("PRAGMA foreign_keys = ON;")


    # def create_tables(self):
    #     try:
    #         # Create Suppliers Table
    #         self.cursor.execute("""
    #             CREATE TABLE IF NOT EXISTS suppliers (
    #                 supplier_id TEXT PRIMARY KEY,
    #                 name TEXT NOT NULL,
    #                 contact TEXT
    #             );
    #         """)

    #         # Create Products Table
    #         self.cursor.execute("""
    #             CREATE TABLE IF NOT EXISTS products (
    #                 product_id TEXT PRIMARY KEY,
    #                 name TEXT NOT NULL,
    #                 category TEXT,
    #                 price REAL NOT NULL,
    #                 quantity INTEGER NOT NULL DEFAULT 0,
    #                 supplier_id TEXT,
    #                 FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    #             );
    #         """)

    #         # Create Orders Table
    #         self.cursor.execute("""
    #             CREATE TABLE IF NOT EXISTS orders (
    #                 order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 product_id TEXT NOT NULL,
    #                 order_type TEXT NOT NULL,
    #                 quantity INTEGER NOT NULL,
    #                 date TEXT NOT NULL,
    #                 supplier_id TEXT,  
    #                 FOREIGN KEY (product_id) REFERENCES products(product_id),
    #                 FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    #             );
    #         """)

    #         self.connection.commit()
    #         logger.info("Database tables created successfully")

    #     except Exception as e:
    #         logger.error(f"Error creating tables: {e}")
        
    def execute_query(self, query, params=()):
        """Write (Insert/Update/Delete) operations"""
        try:
            cursor = self.conn.cursor()  # create fresh cursor
            cursor.execute(query, params)
            self.conn.commit()
            logger.info("DB Write Operation Successful")
            return True
        except Exception as e:
            logger.error(f"DB Write Operation Failed: {e}")
            raise


    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
        logger.info("Database connection closed")
