from __future__ import annotations

from typing import Optional

from app.models.entities import Product


class ProductRepository:
    def __init__(self) -> None:
        self._products: dict[int, Product] = {
            product.id: product for product in self._seed_products()
        }

    def list_all(self) -> list[Product]:
        return sorted(self._products.values(), key=lambda product: product.id)

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    @staticmethod
    def _seed_products() -> list[Product]:
        return [
            Product(
                id=1,
                name="Auriculares Nova X",
                description="Auriculares inalambricos con cancelacion de ruido.",
                price_cents=8999,
                stock=12,
                category="Audio",
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
            ),
            Product(
                id=2,
                name="Teclado TKL Orbit",
                description="Teclado mecanico compacto para productividad y gaming.",
                price_cents=7499,
                stock=8,
                category="Perifericos",
                image_url="https://images.unsplash.com/photo-1511467687858-23d96c32e4ae",
            ),
            Product(
                id=3,
                name="Mouse Pulse Pro",
                description="Mouse ergonomico con sensor de alta precision.",
                price_cents=4599,
                stock=20,
                category="Perifericos",
                image_url="https://images.unsplash.com/photo-1527814050087-3793815479db",
            ),
            Product(
                id=4,
                name="Monitor Vision 27",
                description="Monitor IPS de 27 pulgadas con resolucion QHD.",
                price_cents=21999,
                stock=6,
                category="Pantallas",
                image_url="https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc",
            ),
            Product(
                id=5,
                name="Webcam Focus HD",
                description="Webcam Full HD con microfono dual integrado.",
                price_cents=5299,
                stock=15,
                category="Streaming",
                image_url="https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04",
            ),
        ]
