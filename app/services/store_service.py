from __future__ import annotations

from collections import defaultdict
from typing import Optional

from app.models.entities import CartItem, InventoryError, Order
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository


class StoreService:
    def __init__(
        self,
        product_repository: ProductRepository,
        order_repository: OrderRepository,
    ) -> None:
        self.product_repository = product_repository
        self.order_repository = order_repository

    def list_products(self) -> list[dict[str, object]]:
        return [product.to_dict() for product in self.product_repository.list_all()]

    def get_product(self, product_id: int) -> Optional[dict[str, object]]:
        product = self.product_repository.get_by_id(product_id)
        return product.to_dict() if product else None

    def quote(self, raw_items: list[dict[str, int]]) -> dict[str, object]:
        cart_items = self._build_cart_items(raw_items)
        total_cents = sum(item.subtotal_cents for item in cart_items)
        return {
            "items": [
                {
                    "product_id": item.product.id,
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price_cents": item.product.price_cents,
                    "subtotal_cents": item.subtotal_cents,
                }
                for item in cart_items
            ],
            "total_items": sum(item.quantity for item in cart_items),
            "total_cents": total_cents,
            "total": total_cents / 100,
        }

    def create_order(
        self,
        customer_name: str,
        customer_email: str,
        shipping_address: str,
        raw_items: list[dict[str, int]],
    ) -> dict[str, object]:
        cart_items = self._build_cart_items(raw_items)

        for item in cart_items:
            if item.quantity > item.product.stock:
                raise InventoryError(f"No hay stock suficiente para {item.product.name}.")

        for item in cart_items:
            item.product.reserve(item.quantity)

        order = Order(
            id=0,
            customer_name=customer_name.strip(),
            customer_email=customer_email.strip(),
            shipping_address=shipping_address.strip(),
            items=[item.to_order_item() for item in cart_items],
        )
        return self.order_repository.create(order).to_dict()

    def list_orders(self) -> list[dict[str, object]]:
        return [order.to_dict() for order in self.order_repository.list_all()]

    def dashboard(self) -> dict[str, object]:
        products = self.product_repository.list_all()
        orders = self.order_repository.list_all()
        revenue_cents = sum(order.total_cents for order in orders)
        return {
            "products_count": len(products),
            "orders_count": len(orders),
            "revenue_cents": revenue_cents,
            "revenue": revenue_cents / 100,
            "low_stock": [
                product.to_dict() for product in products if 0 < product.stock <= 5
            ],
        }

    def _build_cart_items(self, raw_items: list[dict[str, int]]) -> list[CartItem]:
        normalized_items = self._merge_quantities(raw_items)
        cart_items: list[CartItem] = []

        for product_id, quantity in normalized_items.items():
            product = self.product_repository.get_by_id(product_id)
            if product is None:
                raise ValueError(f"El producto {product_id} no existe.")
            cart_items.append(CartItem(product=product, quantity=quantity))

        if not cart_items:
            raise ValueError("El carrito no puede estar vacio.")

        return cart_items

    @staticmethod
    def _merge_quantities(raw_items: list[dict[str, int]]) -> dict[int, int]:
        quantities: dict[int, int] = defaultdict(int)

        for item in raw_items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            if quantity <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
            quantities[product_id] += quantity

        return dict(quantities)
