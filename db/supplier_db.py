# ims/db/supplier_db.py

import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import logger
from models.supplier import Supplier
from db.database import Database 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ims.db")


class SupplierDB(Database):

    def __init__(self):
        super().__init__()
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS suppliers (
                     supplier_id TEXT PRIMARY KEY,
                     name TEXT NOT NULL,
                     contact_info TEXT
                 );
             """)

    def add_supplier(self, supplier: Supplier):
        try:
            self.execute_query("""
                INSERT INTO suppliers (supplier_id, name, contact_info)
                VALUES (?, ?, ?)
            """, (supplier.supplier_id, supplier.name, supplier.contact_info))
            logger.info(f"Supplier added to DB: {supplier.supplier_id}")
        except Exception as e:
            logger.error(f"Failed to add supplier: {e}")

    def get_supplier_by_id(self, supplier_id):
        # self.execute_query("SELECT * FROM suppliers WHERE supplier_id = ?", (supplier_id,))
        row = self.fetch_one("SELECT * FROM suppliers WHERE supplier_id = ?", (supplier_id,))

        if row:
            return Supplier(**dict(row))
        return None

    def get_all_suppliers(self):
        # self.execute_query("SELECT * FROM suppliers")
        rows = self.fetch_all("SELECT * FROM suppliers WHERE is_deleted = 0 ORDER BY name")

        return [Supplier(**dict(row)) for row in rows]

    def remove_supplier(self, supplier_id):
        """Soft delete a supplier by marking it as deleted."""
        try:
            # Check if supplier has active products
            products = self.fetch_all(
                "SELECT * FROM products WHERE supplier_id = ? AND is_deleted = 0", (supplier_id,)
            )
            if products:
                raise Exception("Cannot delete supplier with active products. Delete or deactivate those products first.")

            # Soft delete supplier
            self.execute_query(
                "UPDATE suppliers SET is_deleted = 1 WHERE supplier_id = ?", (supplier_id,)
            )

            logger.info(f"Supplier {supplier_id} marked as deleted.")
            return {"message": "Supplier deleted successfully."}

        except Exception as e:
            logger.error(f"Error deleting supplier {supplier_id}: {e}")
            raise

    def soft_delete_supplier(self, supplier_id):
        self.execute_query(
            "UPDATE suppliers SET is_deleted = 1 WHERE supplier_id = ?", (supplier_id,)
        )


    def update_supplier(self, supplier_id, name=None, contact_info=None):
        try:
            update_fields = []
            params = []

            if name:
                update_fields.append("name = ?")
                params.append(name)

            if contact_info:
                update_fields.append("contact_info = ?")
                params.append(contact_info)

            params.append(supplier_id)

            query = f"UPDATE suppliers SET {', '.join(update_fields)} WHERE supplier_id = ?"
            self.execute_query(query, tuple(params))

            logger.info(f"Supplier updated: {supplier_id}")

        except Exception as e:
            logger.error(f"Failed to update supplier: {e}")

if __name__ == "__main__":
    db_supplier = SupplierDB()
    print("SuppliersDB instance created successfully!")