from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

PRODUCTS = {
    1: {"name": "Smartphone X", "price": 800},
    2: {"name": "Laptop Pro", "price": 1200},
    3: {"name": "Headphones", "price": 200},
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cart System</title>
</head>
<body>
    <h1>Shopping Cart</h1>

    <select id="product">
        {% for id, p in products.items() %}
        <option value="{{id}}">{{p['name']}} - ${{p['price']}}</option>
        {% endfor %}
    </select>

    <button onclick="addToCart()">Add to Cart</button>

    <h2>Cart</h2>
    <ul id="cart"></ul>
    <h3 id="total"></h3>

<script>
let cart = JSON.parse(localStorage.getItem("cart")) || {};

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}

function renderCart() {
    fetch("/api/products")
        .then(r => r.json())
        .then(products => {
            let cartList = document.getElementById("cart");
            cartList.innerHTML = "";
            let total = 0;

            for (let id in cart) {
                let item = products[id];
                let qty = cart[id];
                let itemTotal = item.price * qty;
                total += itemTotal;

                cartList.innerHTML += `
                    <li>
                        ${item.name} x ${qty} = $${itemTotal}
                        <button onclick="removeItem(${id})">Remove</button>
                    </li>
                `;
            }

            document.getElementById("total").innerText = "Total: $" + total;
        });
}

function addToCart() {
    let id = document.getElementById("product").value;
    cart[id] = (cart[id] || 0) + 1;
    saveCart();
    syncServer();
    renderCart();
}

function removeItem(id) {
    delete cart[id];
    saveCart();
    syncServer();
    renderCart();
}

function syncServer() {
    fetch("/api/cart", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(cart)
    });
}

function loadCart() {
    fetch("/api/cart")
        .then(r => r.json())
        .then(data => {
            cart = data;
            saveCart();
            renderCart();
        });
}

loadCart();
renderCart();
</script>

</body>
</html>
"""

SERVER_CART = {}

@app.route("/")
def home():
    return render_template_string(HTML, products=PRODUCTS)

@app.route("/api/products")
def get_products():
    return jsonify(PRODUCTS)

@app.route("/api/cart", methods=["GET", "POST"])
def cart():
    global SERVER_CART
    if request.method == "POST":
        SERVER_CART = request.json or {}
        return jsonify({"status": "updated"})
    return jsonify(SERVER_CART)

if __name__ == "__main__":
    app.run(debug=True)