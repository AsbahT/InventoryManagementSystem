from fastapi import APIRouter, Depends, HTTPException
from services.inventory_manager import InventoryManager
from models.order import Order

router = APIRouter(prefix="/orders", tags=["orders"])
def get_manager():
    return InventoryManager()

@router.post("/", response_model=None)
def place_order(order_data: dict,manager: InventoryManager = Depends(get_manager)):
    try:
        # Convert incoming dict into your existing Order model
        order = Order(**order_data)
        manager.place_order(order)
        return {"message": "Order placed successfully"}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_orders(manager: InventoryManager = Depends(get_manager)):
    orders = manager.get_order_history()
    return [vars(o) for o in orders]

@router.get("/{order_id}")
def get_order(order_id: str,manager: InventoryManager = Depends(get_manager)):
    order = manager.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return vars(order)

@router.delete("/{order_id}")
def cancel_order(order_id: str,manager: InventoryManager = Depends(get_manager)):
    try:
        result = manager.cancel_order(order_id)
        return {"success": True, "message": result["message"]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))