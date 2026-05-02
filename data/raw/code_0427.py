"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_000.txt
Run      : 1
"""

from flask import Flask, jsonify, render_template
import random
import time

app = Flask(__name__)

# Mock product data
products = [
    {"id": 1, "name": "Product 1", "price": 100},
    {"id": 2, "name": "Product 2", "price": 200},
]

# Mock product details
product_details = {
    1: {"description": "Description for Product 1", "stock": 20},
    2: {"description": "Description for Product 2", "stock": 10},
}

# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to get all products
@app.route("/api/products")
def get_products():
    return jsonify(products)

# API endpoint to get details of a product
@app.route("/api/product/<int:product_id>/details")
def get_product_details(product_id):
    # Simulate network delay
    time.sleep(0.5)
    return jsonify(product_details.get(product_id, {}))

# API endpoint to update product price
@app.route("/api/product/<int:product_id>/price", methods=["PUT"])
def update_product_price(product_id):
    # Simulate updating price (for demonstration purposes, we'll just return a new random price)
    new_price = random.randint(100, 200)
    # In a real application, you would update your database here
    return jsonify({"price": new_price})

if __name__ == "__main__":
    app.run(debug=True)

# For the template rendering, ensure you have an 'index.html' file in the templates directory
# The content of 'index.html' would be similar to the provided HTML, but with adjustments to make AJAX calls to the Flask API endpoints.

# Example of how 'index.html' might look:
# <html>
# <body>
# <div id="products"></div>
# <script>
# fetch('/api/products')
# .then(response => response.json())
# .then(products => {
#     products.forEach(product => {
#         const productDiv = document.createElement('div');
#         productDiv.innerHTML = `
#             <h2>${product.name}</h2>
#             <p>Price: $<span class="price">${product.price}</span></p>
#             <button onclick="loadDetails(${product.id})">View Details</button>
#             <div id="details-${product.id}" class="product-details"></div>
#         `;
#         document.getElementById('products').appendChild(productDiv);
#     });
# });
# 
# function loadDetails(productId) {
#     fetch(`/api/product/${productId}/details`)
#     .then(response => response.json())
#     .then(details => {
#         const detailsDiv = document.getElementById(`details-${productId}`);
#         detailsDiv.innerHTML = `
#             <p>Description: ${details.description}</p>
#             <p>Stock: ${details.stock}</p>
#         `;
#         detailsDiv.style.display = 'block';
#     });
# }
# </script>
# </body>
# </html>