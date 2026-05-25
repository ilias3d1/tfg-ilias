# Tienda online con FastAPI y JavaScript

Aplicacion web de ventas de productos online construida con `Python`, `FastAPI`,
POO en el backend y frontend en `JavaScript` puro.

## Incluye

- Catalogo de productos con stock.
- Carrito persistido en `localStorage`.
- Checkout y creacion de pedidos.
- Resumen con numero de productos, pedidos e ingresos.
- Arquitectura separada en `models`, `repositories`, `services` y `api`.

## Estructura

```text
app/
  api/
  models/
  repositories/
  schemas/
  services/
frontend/static/
```

## Ejecutar

1. Crear entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Lanzar el servidor:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Abrir en el navegador:

   [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Endpoints

- `GET /api/health`
- `GET /api/products`
- `GET /api/products/{product_id}`
- `POST /api/cart/quote`
- `POST /api/orders`
- `GET /api/orders`
- `GET /api/dashboard`