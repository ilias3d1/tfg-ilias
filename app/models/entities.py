from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


class InventoryError(ValueError):
    """Se lanza cuando el stock no permite completar una operacion."""


@dataclass
class Product:
    id: int
    name: str
    description: str
    price_cents: int
    stock: int
    category: str
    image_url: str

    def reserve(self, quantity: int) -> None:
        if quantity <= 0:
            raise InventoryError("La cantidad debe ser mayor que cero.")
        if quantity > self.stock:
            raise InventoryError(f"No hay stock suficiente para {self.name}.")
        self.stock -= quantity

    def restore(self, quantity: int) -> None:
        if quantity > 0:
            self.stock += quantity

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price_cents": self.price_cents,
            "price": self.price_cents / 100,
            "stock": self.stock,
            "category": self.category,
            "image_url": self.image_url,
        }


@dataclass
class CartItem:
    product: Product
    quantity: int

    @property
    def subtotal_cents(self) -> int:
        return self.product.price_cents * self.quantity

    def to_order_item(self) -> "OrderItem":
        return OrderItem(
            product_id=self.product.id,
            name=self.product.name,
            unit_price_cents=self.product.price_cents,
            quantity=self.quantity,
        )


@dataclass
class OrderItem:
    product_id: int
    name: str
    unit_price_cents: int
    quantity: int

    @property
    def subtotal_cents(self) -> int:
        return self.unit_price_cents * self.quantity

    def to_dict(self) -> dict[str, object]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "unit_price_cents": self.unit_price_cents,
            "unit_price": self.unit_price_cents / 100,
            "quantity": self.quantity,
            "subtotal_cents": self.subtotal_cents,
            "subtotal": self.subtotal_cents / 100,
        }


@dataclass
class Order:
    id: int
    customer_name: str
    customer_email: str
    shipping_address: str
    items: list[OrderItem]
    status: str = "confirmed"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def total_cents(self) -> int:
        return sum(item.subtotal_cents for item in self.items)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "shipping_address": self.shipping_address,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "total_items": self.total_items,
            "total_cents": self.total_cents,
            "total": self.total_cents / 100,
            "items": [item.to_dict() for item in self.items],
        }
