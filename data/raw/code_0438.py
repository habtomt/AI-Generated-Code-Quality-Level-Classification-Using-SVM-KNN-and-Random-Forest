"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import json
import os
from flask import Flask, render_template, request, jsonify
from flask_session import Session

# Initialize Flask app
app = Flask(__name__)

# Configure session settings
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Sample data for cart items
sample_data = [
    {"id": 1, "name": "Product 1", "price": 10.99},
    {"id": 2, "name": "Product 2", "price": 9.99},
    {"id": 3, "name": "Product 3", "price": 19.99},
]

# Initialize cart in memory
cart = []

# Load cart from cache file
if os.path.exists("cart_cache.json"):
    try:
        with open("cart_cache.json", "r") as f:
            cart = json.load(f)
    except Exception as e:
        print(f"Error loading cart cache: {e}")

# Route for displaying the cart
@app.route("/cart")
def display_cart():
    total = 0
    for item in cart:
        total += item["price"] * item["quantity"]
    return render_template("cart.html", cart=cart, total=total)

# Route for updating the cart using AJAX
@app.route("/update_cart", methods=["POST"])
def update_cart():
    data = request.json
    item_id = data["item_id"]
    operation = data["operation"]
    
    # Find the item in the cart
    for i, item in enumerate(cart):
        if item["id"] == item_id:
            if operation == "add":
                item["quantity"] += 1
            elif operation == "remove":
                item["quantity"] -= 1
                if item["quantity"] <= 0:
                    cart.pop(i)
            elif operation == "update_quantity":
                item["quantity"] = data["quantity"]
            break
    
    # Save cart to cache file
    with open("cart_cache.json", "w") as f:
        json.dump(cart, f)
    
    return jsonify({"success": True})

# Route for adding an item to the cart
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    data = request.json
    item_id = data["item_id"]
    quantity = data["quantity"]
    
    # Find the item in the sample data
    for item in sample_data:
        if item["id"] == item_id:
            cart.append({"id": item_id, "name": item["name"], "price": item["price"], "quantity": quantity})
            # Save cart to cache file
            with open("cart_cache.json", "w") as f:
                json.dump(cart, f)
            return jsonify({"success": True})
            break
    
    return jsonify({"success": False})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)