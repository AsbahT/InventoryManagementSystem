from fastapi import FastAPI
from api.routes.products_api import router as products_router
from api.routes.suppliers_api import router as suppliers_router
from api.routes.orders_api import router as orders_router

app = FastAPI(title="Inventory Management API")

# Register API routes
app.include_router(products_router)
app.include_router(suppliers_router)
app.include_router(orders_router)

@app.get("/")
def root():
    return {"message": "Inventory API is running "}
