import sqlite3,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.inventory_manager import InventoryManager
from models.supplier import Supplier
from models.product import Product
from models.order import Order

def test_orders_workflow():
    print("\n Running Orders Workflow Test...\n")

    manager = InventoryManager()
    manager.orders_db.execute_query("DELETE FROM orders")
    # manager.orders_db.commit()


    #  Add supplier
    supplier = Supplier("S100", "Lenovo", "contact@lenovo.com")
    try:
        manager.add_supplier(supplier)
    except:
        print("Supplier already exists (OK)")

    #  Add product
    product = Product("P100", "Laptop ThinkPad", "Electronics", 90000, 10, "S100")
    try:
        manager.add_product(product)
    except:
        print("Product already exists (OK)")

    #  Purchase (increase stock)
    order1 = Order("P100", "purchase", 5, "2025-10-01", "S100")
    manager.place_order(order1)

    #  Sale (decrease stock)
    order2 = Order("P100", "sale", 3, "2025-10-02", None)
    manager.place_order(order2)

    #  Display updated inventory
    inventory = manager.get_inventory()
    print("\n🧾 Inventory After Orders:")
    for p in inventory:
        print(p)

    #  Display order history
    orders = manager.get_order_history()
    print("\n Order History:")
    for o in orders:
        print(o)

    print("\n Test Completed Successfully \n")


if __name__ == "__main__":
    test_orders_workflow()
