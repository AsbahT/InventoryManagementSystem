# from database import Database

# db = Database()

# # Add soft-delete column to products
# db.execute_query("ALTER TABLE products ADD COLUMN is_deleted INTEGER DEFAULT 0;")

# # Add soft-delete column to suppliers
# db.execute_query("ALTER TABLE suppliers ADD COLUMN is_deleted INTEGER DEFAULT 0;")

# # Add status column to orders
# db.execute_query("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'active';")

# print("Migration completed successfully!")


# # import sqlite3
# # import os
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # DB_NAME = os.path.join(BASE_DIR, "ims.db")
# # # DB_PATH = r"ims.db"   # <-- change only if needed

# # def inspect_database(db_path):
# #     print("\n==============================")
# #     print(" Database Inspection Report")
# #     print("==============================\n")

# #     # Check if file exists
# #     if not os.path.exists(db_path):
# #         print(f" ERROR: Database file not found: {db_path}")
# #         return

# #     # Print file details
# #     print(f" Database Path: {os.path.abspath(db_path)}")
# #     size = os.path.getsize(db_path) / 1024
# #     print(f" Database Size: {size:.2f} KB")

# #     # Connect
# #     conn = sqlite3.connect(db_path)
# #     conn.row_factory = sqlite3.Row
# #     cursor = conn.cursor()

# #     # Retrieve all tables
# #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# #     tables = [row[0] for row in cursor.fetchall()]

# #     if not tables:
# #         print("\n No tables found in this database.")
# #         conn.close()
# #         return

# #     print("\n Tables Found:")
# #     for t in tables:
# #         print(f"  - {t}")

# #     print("\n------------------------------")

# #     # Loop through tables to show schema + row count
# #     for table in tables:
# #         print(f"\n Table: {table}")

# #         # Show schema
# #         cursor.execute(f"PRAGMA table_info({table});")
# #         columns = cursor.fetchall()

# #         print("   Columns:")
# #         for col in columns:
# #             cid, name, type_, notnull, dflt, pk = col
# #             print(f"     - {name} ({type_})"
# #                   f"{' PRIMARY KEY' if pk else ''}"
# #                   f"{' NOT NULL' if notnull else ''}"
# #                   f"{' DEFAULT '+str(dflt) if dflt else ''}")

# #         # Row count
# #         cursor.execute(f"SELECT COUNT(*) FROM {table}")
# #         count = cursor.fetchone()[0]
# #         print(f"   Rows: {count}")

# #         # Foreign keys
# #         cursor.execute(f"PRAGMA foreign_key_list({table});")
# #         fk_list = cursor.fetchall()

# #         if fk_list:
# #             print("   Foreign Keys:")
# #             for fk in fk_list:
# #                 print(f"     - {fk[3]} → {fk[2]}.{fk[4]}")
# #         else:
# #             print("   Foreign Keys: None")

# #         print("\n------------------------------")

# #     conn.close()
# #     print("\n Inspection Complete.\n")


# # # Run the inspector
# # inspect_database(DB_NAME)



# run_migrations.py
import os
from database import Database

db = Database()

def table_exists(table_name):
    result = db.fetch_all(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table_name,)
    )
    return len(result) > 0


def column_exists(table_name, column_name):
    columns = db.fetch_all(f"PRAGMA table_info({table_name});")
    return any(col[1] == column_name for col in columns)


def add_column_if_not_exists(table, column, definition):
    """
    Adds a column only if missing.
    Example:
        add_column_if_not_exists("products", "is_deleted", "INTEGER DEFAULT 0")
    """
    if not column_exists(table, column):
        print(f"[MIGRATION] Adding column '{column}' to '{table}'...")
        db.execute_query(f"ALTER TABLE {table} ADD COLUMN {column} {definition};")
        print(f"[OK] Added '{column}'.")
    else:
        print(f"[SKIP] Column '{column}' already exists on '{table}'.")


def create_tables_if_not_exist():
    # Example: Create products table
    if not table_exists("products"):
        print("[MIGRATION] Creating 'products' table...")
        db.execute_query("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                supplier_id INTEGER,
                is_deleted INTEGER DEFAULT 0
            );
        """)
        print("[OK] Created 'products' table.")
    else:
        print("[SKIP] Table 'products' already exists.")

    # Example: Create suppliers table
    if not table_exists("suppliers"):
        print("[MIGRATION] Creating 'suppliers' table...")
        db.execute_query("""
            CREATE TABLE suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                is_deleted INTEGER DEFAULT 0
            );
        """)
        print("[OK] Created 'suppliers' table.")
    else:
        print("[SKIP] Table 'suppliers' already exists.")


def run():
    print("\n=== Running Migrations ===")

    # Ensure tables exist
    create_tables_if_not_exist()

    # Ensure missing columns are added safely
    add_column_if_not_exists("products", "is_deleted", "INTEGER DEFAULT 0")
    add_column_if_not_exists("suppliers", "is_deleted", "INTEGER DEFAULT 0")

    print("=== Migrations Complete ===\n")


if __name__ == "__main__":
    run()
