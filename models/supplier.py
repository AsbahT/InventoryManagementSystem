# ims/models/supplier.py

from utils.logging_config import logger

class Supplier:
    def __init__(self, supplier_id, name, contact_info):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info

        logger.info(f"Created Supplier: {name} (ID: {supplier_id})")

    def update_contact(self, new_contact):
        old_contact = self.contact_info
        self.contact_info = new_contact

        logger.info(
            f"Updated contact for Supplier {self.supplier_id} "
            f"from '{old_contact}' to '{new_contact}'"
        )

    def display_info(self):
        """Optional: view supplier details (good for UI/CLI output)"""
        logger.info(f"Displaying Supplier details for {self.supplier_id}")
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Name: {self.name}")
        print(f"Contact: {self.contact_info}")
