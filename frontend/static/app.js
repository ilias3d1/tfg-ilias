class StoreApi {
  async request(path, options = {}) {
    const response = await fetch(path, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(payload.detail || "No se pudo completar la operacion.");
    }

    return payload;
  }

  getProducts() {
    return this.request("/api/products");
  }

  getDashboard() {
    return this.request("/api/dashboard");
  }

  getOrders() {
    return this.request("/api/orders");
  }

  getQuote(items) {
    return this.request("/api/cart/quote", {
      method: "POST",
      body: JSON.stringify({ items }),
    });
  }

  checkout(payload) {
    return this.request("/api/orders", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }
}

class Cart {
  constructor(storageKey = "online-store-cart") {
    this.storageKey = storageKey;
    this.items = new Map();
    this.load();
  }

  load() {
    try {
      const savedItems = JSON.parse(localStorage.getItem(this.storageKey) || "[]");
      this.items = new Map(
        savedItems
          .filter((item) => Number.isInteger(item.product_id) && item.quantity > 0)
          .map((item) => [item.product_id, item.quantity]),
      );
    } catch {
      this.items = new Map();
    }
  }

  save() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.getItems()));
  }

  add(productId) {
    const quantity = this.items.get(productId) || 0;
    this.items.set(productId, quantity + 1);
    this.save();
  }

  update(productId, quantity) {
    if (quantity <= 0) {
      this.remove(productId);
      return;
    }

    this.items.set(productId, quantity);
    this.save();
  }

  remove(productId) {
    this.items.delete(productId);
    this.save();
  }

  clear() {
    this.items.clear();
    this.save();
  }

  getItems() {
    return Array.from(this.items.entries()).map(([product_id, quantity]) => ({
      product_id,
      quantity,
    }));
  }
}

class StoreUI {
  constructor(api, cart) {
    this.api = api;
    this.cart = cart;
    this.products = [];
    this.productMap = new Map();
    this.elements = {
      products: document.querySelector("#products"),
      cartItems: document.querySelector("#cart-items"),
      cartState: document.querySelector("#cart-state"),
      quoteItems: document.querySelector("#quote-items"),
      quoteTotal: document.querySelector("#quote-total"),
      orders: document.querySelector("#orders"),
      productsCount: document.querySelector("#products-count"),
      ordersCount: document.querySelector("#orders-count"),
      revenueTotal: document.querySelector("#revenue-total"),
      checkoutForm: document.querySelector("#checkout-form"),
      checkoutButton: document.querySelector("#checkout-button"),
      feedback: document.querySelector("#feedback"),
      customerName: document.querySelector("#customer-name"),
      customerEmail: document.querySelector("#customer-email"),
      shippingAddress: document.querySelector("#shipping-address"),
    };
  }

  async init() {
    this.bindEvents();
    await Promise.all([
      this.loadProducts(),
      this.refreshDashboard(),
      this.refreshOrders(),
    ]);
    this.renderCart();
    await this.refreshQuote();
  }

  bindEvents() {
    this.elements.checkoutForm.addEventListener("submit", (event) =>
      this.handleCheckout(event),
    );
  }

  async loadProducts() {
    this.products = await this.api.getProducts();
    this.productMap = new Map(this.products.map((product) => [product.id, product]));
    this.renderProducts();
  }

  renderProducts() {
    if (this.products.length === 0) {
      this.elements.products.innerHTML =
        '<div class="empty-state">No hay productos disponibles.</div>';
      return;
    }

    this.elements.products.innerHTML = this.products
      .map(
        (product) => `
          <article class="product-card">
            <img src="${product.image_url}" alt="${product.name}" />
            <div class="product-meta">
              <span class="badge">${product.category}</span>
              <span class="stock-label">Stock: ${product.stock}</span>
            </div>
            <div>
              <h3>${product.name}</h3>
              <p>${product.description}</p>
            </div>
            <div class="product-meta">
              <strong class="price">${this.formatCurrency(product.price)}</strong>
              <button data-add-product="${product.id}" ${
                product.stock === 0 ? "disabled" : ""
              }>
                ${product.stock === 0 ? "Sin stock" : "Anadir"}
              </button>
            </div>
          </article>
        `,
      )
      .join("");

    this.elements.products
      .querySelectorAll("[data-add-product]")
      .forEach((button) => {
        button.addEventListener("click", async () => {
          const productId = Number(button.dataset.addProduct);
          this.cart.add(productId);
          this.renderCart();
          await this.refreshQuote();
        });
      });
  }

  renderCart() {
    const items = this.cart.getItems();
    if (items.length === 0) {
      this.elements.cartItems.innerHTML =
        '<div class="empty-state">Todavia no has anadido productos.</div>';
      this.elements.cartState.textContent = "Tu carrito esta vacio.";
      return;
    }

    this.elements.cartItems.innerHTML = items
      .map(({ product_id, quantity }) => {
        const product = this.productMap.get(product_id);
        if (!product) {
          return "";
        }

        return `
          <article class="cart-item">
            <div class="cart-item-header">
              <div>
                <strong>${product.name}</strong>
                <p>${this.formatCurrency(product.price)} x ${quantity}</p>
              </div>
              <strong>${this.formatCurrency(product.price * quantity)}</strong>
            </div>
            <div class="cart-actions">
              <button class="secondary-button" data-cart-action="decrease" data-product-id="${product_id}">-1</button>
              <button class="secondary-button" data-cart-action="increase" data-product-id="${product_id}">+1</button>
              <button class="danger-button" data-cart-action="remove" data-product-id="${product_id}">Quitar</button>
            </div>
          </article>
        `;
      })
      .join("");

    this.elements.cartState.textContent = `${items.length} referencias en el carrito.`;
    this.bindCartActions();
  }

  bindCartActions() {
    this.elements.cartItems
      .querySelectorAll("[data-cart-action]")
      .forEach((button) => {
        button.addEventListener("click", async () => {
          const productId = Number(button.dataset.productId);
          const action = button.dataset.cartAction;
          const currentItem = this.cart.getItems().find(
            (item) => item.product_id === productId,
          );

          if (!currentItem) {
            return;
          }

          if (action === "increase") {
            this.cart.update(productId, currentItem.quantity + 1);
          }
          if (action === "decrease") {
            this.cart.update(productId, currentItem.quantity - 1);
          }
          if (action === "remove") {
            this.cart.remove(productId);
          }

          this.renderCart();
          await this.refreshQuote();
        });
      });
  }

  async refreshQuote() {
    const items = this.cart.getItems();
    if (items.length === 0) {
      this.elements.quoteItems.textContent = "0";
      this.elements.quoteTotal.textContent = this.formatCurrency(0);
      return;
    }

    try {
      const quote = await this.api.getQuote(items);
      this.elements.quoteItems.textContent = String(quote.total_items);
      this.elements.quoteTotal.textContent = this.formatCurrency(quote.total);
      this.setFeedback("");
    } catch (error) {
      this.elements.quoteItems.textContent = "0";
      this.elements.quoteTotal.textContent = this.formatCurrency(0);
      this.setFeedback(error.message, true);
    }
  }

  async refreshDashboard() {
    const dashboard = await this.api.getDashboard();
    this.elements.productsCount.textContent = String(dashboard.products_count);
    this.elements.ordersCount.textContent = String(dashboard.orders_count);
    this.elements.revenueTotal.textContent = this.formatCurrency(dashboard.revenue);
  }

  async refreshOrders() {
    const orders = await this.api.getOrders();

    if (orders.length === 0) {
      this.elements.orders.innerHTML =
        '<div class="empty-state">Aun no se ha registrado ningun pedido.</div>';
      return;
    }

    this.elements.orders.innerHTML = orders
      .map(
        (order) => `
          <article class="order-card">
            <div class="order-card-header">
              <div>
                <strong>Pedido #${order.id}</strong>
                <p>${order.customer_name} · ${order.customer_email}</p>
              </div>
              <strong>${this.formatCurrency(order.total)}</strong>
            </div>
            <p>${order.shipping_address}</p>
            <div class="order-items">
              ${order.items
                .map(
                  (item) =>
                    `<span>${item.quantity} x ${item.name} · ${this.formatCurrency(item.subtotal)}</span>`,
                )
                .join("")}
            </div>
          </article>
        `,
      )
      .join("");
  }

  async handleCheckout(event) {
    event.preventDefault();

    const items = this.cart.getItems();
    if (items.length === 0) {
      this.setFeedback("Anade productos al carrito antes de comprar.", true);
      return;
    }

    this.elements.checkoutButton.disabled = true;

    try {
      await this.api.checkout({
        customer_name: this.elements.customerName.value.trim(),
        customer_email: this.elements.customerEmail.value.trim(),
        shipping_address: this.elements.shippingAddress.value.trim(),
        items,
      });

      this.elements.checkoutForm.reset();
      this.cart.clear();
      this.renderCart();
      await Promise.all([
        this.loadProducts(),
        this.refreshDashboard(),
        this.refreshOrders(),
      ]);
      await this.refreshQuote();
      this.setFeedback("Pedido creado correctamente.");
    } catch (error) {
      this.setFeedback(error.message, true);
    } finally {
      this.elements.checkoutButton.disabled = false;
    }
  }

  setFeedback(message, isError = false) {
    this.elements.feedback.textContent = message;
    this.elements.feedback.classList.toggle("error", isError);
  }

  formatCurrency(value) {
    return new Intl.NumberFormat("es-ES", {
      style: "currency",
      currency: "EUR",
    }).format(value);
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  const app = new StoreUI(new StoreApi(), new Cart());
  await app.init();
});
