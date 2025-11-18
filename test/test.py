# import sqlite3

# conn = sqlite3.connect("ims.db")
# cursor = conn.cursor()

# cursor.execute("PRAGMA table_info(orders)")
# print(cursor.fetchall())

# conn.close()
# import sqlite3
# conn = sqlite3.connect("ims.db")
# cursor = conn.cursor()
# cursor.execute("SELECT order_id, order_type FROM orders")
# print(cursor.fetchall())
# conn.close()

import sqlite3

conn = sqlite3.connect("ims.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(orders)")
print(cursor.fetchall())
conn.close()


