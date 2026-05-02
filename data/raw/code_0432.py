"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_000.txt
Run      : 2
"""

# Import the required libraries
import json
import requests
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# Define the Product schema for JSON output
class ProductSchema:
    def __init__(self, id, name, price, description, image_url):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url

# Initialize the API key (replace with your actual API key)
API_KEY = "YOUR_API_KEY"

# Route to render the product list
@app.route('/')
def index():
    try:
        # Fetch products from the database
        products = Product.query.all()
        product_schema = [ProductSchema(**product.__dict__) for product in products]
        return render_template('index.html', products=product_schema)
    except Exception as e:
        return str(e)

# Route to handle AJAX requests for product details
@app.route('/product/<int:id>')
def get_product(id):
    try:
        # Fetch product details from the database
        product = Product.query.get(id)
        if product:
            product_schema = ProductSchema(**product.__dict__)
            # Simulate real-time price updates using a fake API call
            price_response = requests.get(f"https://api.example.com/price?product_id={id}&api_key={API_KEY}")
            price_data = json.loads(price_response.text)
            product_schema.price = price_data['price']
            return jsonify(product_schema.__dict__)
        else:
            return jsonify({"error": "Product not found"})
    except Exception as e:
        return str(e)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)