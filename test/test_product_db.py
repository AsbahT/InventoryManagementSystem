import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.product import Product
from db.product_db import ProductDB

db = ProductDB()

p1 = Product("P001", "Keyboard", "Electronics", 1200, 10, "S001")
db.add_product(p1)

product = db.get_product_by_id("P001")
print(product)

db.update_stock("P001", 20)

all_products = db.get_all_products()
for p in all_products:
    print(p)

db.close()
