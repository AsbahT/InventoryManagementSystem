from fastapi import APIRouter, Depends, HTTPException
from services.inventory_manager import InventoryManager
from models.product import Product

router = APIRouter(prefix="/products", tags=["products"])
# manager = InventoryManager()
def get_manager():
    return InventoryManager()

@router.get("/")
def list_products(manager: InventoryManager = Depends(get_manager)):
    products = manager.get_inventory()
    return [vars(p) for p in products]

@router.post("/", response_model=None)
def add_product(product_data: dict,manager: InventoryManager = Depends(get_manager)):  # Receive raw dict
    try:
        # Convert dict to your Python class manually
        product = Product(**product_data)
        manager.add_product(product)
        return {"message": "Product added successfully"}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/{product_id}")
def get_product(product_id: str,manager: InventoryManager = Depends(get_manager)):
    product = manager.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return vars(product)

@router.delete("/{product_id}")
def delete_product(product_id: str,manager: InventoryManager = Depends(get_manager)):
    """Delete a product by ID."""
    try:
        manager.remove_product(product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))