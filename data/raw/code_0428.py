"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_001.txt
Run      : 1
"""

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize cart as an empty dictionary
cart = {}

# Function to update cart in memory
def update_cart(item_name, price, action):
    global cart
    if item_name in cart:
        if action == 'remove':
            del cart[item_name]
        elif action == 'add':
            cart[item_name] = price
    else:
        cart[item_name] = price

# Function to calculate total price
def calculate_total():
    global cart
    total = sum(cart.values())
    return total

# API endpoint to add an item to the cart
@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        item_name = data['item_name']
        price = data['price']
        update_cart(item_name, price, 'add')
        return jsonify({'message': f'Item {item_name} added to the cart', 'total': calculate_total()})
    except Exception as e:
        return jsonify({'error': str(e)})

# API endpoint to remove an item from the cart
@app.route('/remove_item', methods=['POST'])
def remove_item():
    try:
        data = request.get_json()
        item_name = data['item_name']
        update_cart(item_name, None, 'remove')
        return jsonify({'message': f'Item {item_name} removed from the cart', 'total': calculate_total()})
    except Exception as e:
        return jsonify({'error': str(e)})

# API endpoint to get the cart
@app.route('/get_cart', methods=['GET'])
def get_cart():
    try:
        return jsonify({'cart': cart, 'total': calculate_total()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

# Client-side caching example using Python's requests library
import requests
import json

def add_item_to_cart(item_name, price):
    try:
        url = 'http://localhost:5000/add_item'
        data = {'item_name': item_name, 'price': price}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f'Item {item_name} added to the cart')
        else:
            print('Error adding item to the cart')
    except Exception as e:
        print(str(e))

def remove_item_from_cart(item_name):
    try:
        url = 'http://localhost:5000/remove_item'
        data = {'item_name': item_name}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f'Item {item_name} removed from the cart')
        else:
            print('Error removing item from the cart')
    except Exception as e:
        print(str(e))

def get_cart():
    try:
        url = 'http://localhost:5000/get_cart'
        response = requests.get(url)
        if response.status_code == 200:
            print('Cart:', response.json())
        else:
            print('Error getting cart')
    except Exception as e:
        print(str(e))

# Example usage
add_item_to_cart('Example Item', 9.99)
get_cart()
remove_item_from_cart('Example Item')
get_cart()