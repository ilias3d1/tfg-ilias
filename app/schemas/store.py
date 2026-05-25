from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class CartLineInput(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class QuoteRequest(BaseModel):
    items: list[CartLineInput] = Field(min_length=1)


class CheckoutRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=80)
    customer_email: str = Field(min_length=5, max_length=120)
    shipping_address: str = Field(min_length=8, max_length=180)
    items: list[CartLineInput] = Field(min_length=1)

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Introduce un email valido.")
        return email


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price_cents: int
    price: float
    stock: int
    category: str
    image_url: str


class QuoteItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    unit_price_cents: int
    subtotal_cents: int


class QuoteResponse(BaseModel):
    items: list[QuoteItemResponse]
    total_items: int
    total_cents: int
    total: float


class OrderItemResponse(BaseModel):
    product_id: int
    name: str
    unit_price_cents: int
    unit_price: float
    quantity: int
    subtotal_cents: int
    subtotal: float


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    shipping_address: str
    status: str
    created_at: str
    total_items: int
    total_cents: int
    total: float
    items: list[OrderItemResponse]


class DashboardResponse(BaseModel):
    products_count: int
    orders_count: int
    revenue_cents: int
    revenue: float
    low_stock: list[ProductResponse]
