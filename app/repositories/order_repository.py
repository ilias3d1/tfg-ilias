from __future__ import annotations

from app.models.entities import Order


class OrderRepository:
    def __init__(self) -> None:
        self._orders: list[Order] = []
        self._next_id = 1

    def create(self, order: Order) -> Order:
        order.id = self._next_id
        self._next_id += 1
        self._orders.append(order)
        return order

    def list_all(self) -> list[Order]:
        return list(reversed(self._orders))
