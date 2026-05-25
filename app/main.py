from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.admin import router as admin_router
from app.api.routes import build_store_router
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.store_service import StoreService


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"

product_repository = ProductRepository()
order_repository = OrderRepository()
store_service = StoreService(product_repository, order_repository)

app = FastAPI(
    title="Tienda Online",
    description="Backend FastAPI para una tienda online orientada a POO.",
    version="1.0.0",
)
app.include_router(build_store_router(store_service))
app.include_router(admin_router)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
