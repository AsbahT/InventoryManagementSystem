# main.py

from services.inventory_manager import InventoryManager
from models.product import Product
from models.supplier import Supplier
from models.order import Order

def main():
    inventory = InventoryManager()

    while True:
        print("\n=== Inventory Management System ===")
        print("1. Add Product")
        print("2. Add Supplier")
        print("3. Place Order")
        print("4. View Product Stock")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            pid = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            category = input("Enter Category: ")
            price = float(input("Enter Price: "))
            qty = int(input("Enter Initial Quantity: "))
            sid = input("Enter Supplier ID: ")

            product = Product(pid, name, category, price, qty, sid)
            inventory.add_product(product)
            print("Product added successfully!")

        elif choice == "2":
            sid = input("Enter Supplier ID: ")
            name = input("Enter Supplier Name: ")
            contact = input("Enter Contact Info: ")

            supplier = Supplier(sid, name, contact)
            inventory.add_supplier(supplier)
            print("Supplier added successfully!")

        elif choice == "3":
            oid = input("Enter Order ID: ")
            pid = input("Enter Product ID: ")
            qty = int(input("Enter Quantity: "))
            order_type = input("Enter Order Type (purchase/sale): ").lower()

            try:
                order = Order(oid, pid, qty, order_type)
                inventory.place_order(order)
                print("Order processed successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            pid = input("Enter Product ID to check stock: ")
            product = inventory.get_product(pid)

            if product:
                print(f"{product.name}: {product.quantity} units")
            else:
                print("Product not found!")

        elif choice == "5":
            print("Exiting System...")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
