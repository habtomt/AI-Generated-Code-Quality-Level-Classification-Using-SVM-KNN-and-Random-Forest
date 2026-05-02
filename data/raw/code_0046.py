from flask import Flask, jsonify, request, render_template_string
import random
import time

app = Flask(__name__)

PRODUCTS = {
    1: {"name": "Smartphone X", "price": 799, "desc": "High-end smartphone with OLED display."},
    2: {"name": "Laptop Pro", "price": 1299, "desc": "Powerful laptop for professionals."},
    3: {"name": "Wireless Headphones", "price": 199, "desc": "Noise-cancelling over-ear headphones."},
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Product UI</title>
</head>
<body>
    <h1>Product Catalog</h1>

    <select id="productSelect">
        {% for id, p in products.items() %}
        <option value="{{id}}">{{p['name']}}</option>
        {% endfor %}
    </select>

    <div id="productDetails"></div>
    <div id="priceBox"></div>

<script>
let currentProductId = document.getElementById("productSelect").value;

document.getElementById("productSelect").addEventListener("change", function() {
    currentProductId = this.value;
    loadProduct();
});

function loadProduct() {
    fetch(`/api/product/${currentProductId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("productDetails").innerHTML =
                `<h2>${data.name}</h2><p>${data.desc}</p>`;
        });
}

function loadPrice() {
    fetch(`/api/price/${currentProductId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("priceBox").innerHTML =
                `<h3>Price: $${data.price}</h3>`;
        });
}

loadProduct();
loadPrice();

setInterval(loadPrice, 3000);
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, products=PRODUCTS)

@app.route("/api/product/<int:pid>")
def product(pid):
    return jsonify(PRODUCTS.get(pid, {}))

@app.route("/api/price/<int:pid>")
def price(pid):
    if pid in PRODUCTS:
        PRODUCTS[pid]["price"] += random.randint(-5, 5)
        return jsonify({"price": PRODUCTS[pid]["price"]})
    return jsonify({"price": 0})

if __name__ == "__main__":
    app.run(debug=True)