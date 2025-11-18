from fastapi import APIRouter, Depends, HTTPException
from services.inventory_manager import InventoryManager
from models.supplier import Supplier

router = APIRouter(prefix="/suppliers", tags=["suppliers"])
# manager = InventoryManager()

def get_manager():
    return InventoryManager()

@router.get("/")
def list_suppliers(manager: InventoryManager = Depends(get_manager)):
    suppliers = manager.get_all_suppliers()
    return [vars(s) for s in suppliers]

@router.post("/", response_model=None)
def add_supplier(supplier_data: dict,manager: InventoryManager = Depends(get_manager)):
    try:
        supplier = Supplier(**supplier_data)
        manager.add_supplier(supplier)
        return {"message": "Supplier added successfully"}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{supplier_id}")
def get_supplier(supplier_id: str,manager: InventoryManager = Depends(get_manager)):
    supplier = manager.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return vars(supplier)

@router.delete("{supplier_id}")
def delete_supplier(supplier_id: str,manager: InventoryManager = Depends(get_manager)):
    try:
        result = manager.remove_supplier(supplier_id)
        return {"success": True, "message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
