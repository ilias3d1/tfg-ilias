from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.models.entities import InventoryError
from app.schemas.store import (
    CheckoutRequest,
    DashboardResponse,
    OrderResponse,
    ProductResponse,
    QuoteRequest,
    QuoteResponse,
)
from app.services.store_service import StoreService


def build_store_router(store_service: StoreService) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["store"])

    @router.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/products", response_model=list[ProductResponse])
    def list_products() -> list[dict[str, object]]:
        return store_service.list_products()

    @router.get("/products/{product_id}", response_model=ProductResponse)
    def get_product(product_id: int) -> dict[str, object]:
        product = store_service.get_product(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado.",
            )
        return product

    @router.post("/cart/quote", response_model=QuoteResponse)
    def quote_order(payload: QuoteRequest) -> dict[str, object]:
        try:
            return store_service.quote([item.model_dump() for item in payload.items])
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
    def create_order(payload: CheckoutRequest) -> dict[str, object]:
        try:
            return store_service.create_order(
                customer_name=payload.customer_name,
                customer_email=payload.customer_email,
                shipping_address=payload.shipping_address,
                raw_items=[item.model_dump() for item in payload.items],
            )
        except InventoryError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.get("/orders", response_model=list[OrderResponse])
    def list_orders() -> list[dict[str, object]]:
        return store_service.list_orders()

    @router.get("/dashboard", response_model=DashboardResponse)
    def dashboard() -> dict[str, object]:
        return store_service.dashboard()

    return router
