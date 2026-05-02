"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import json
import requests

class Cart:
    def __init__(self):
        # Initialize cart dictionary with items and totals
        self.cart = {
            'items': {},
            'subtotal': 0,
            'tax': 0,
            'shipping': 0,
            'total': 0
        }
        self.cache = {}  # In-memory cache for cart state

    def get_cart(self, cart_id):
        """Retrieve cart from cache or API"""
        if cart_id in self.cache:
            return self.cache[cart_id]  # Return cached cart
        try:
            # Simulate API request to retrieve cart
            response = requests.get(f'https://api.example.com/cart/{cart_id}')
            response.raise_for_status()  # Raise exception for HTTP errors
            cart_data = response.json()
            # Store cart in cache
            self.cache[cart_id] = cart_data
            return cart_data
        except requests.RequestException as e:
            print(f"Error retrieving cart: {e}")
            return None

    def update_cart(self, cart_id, item_id, action):
        """Update cart item and recalculate totals"""
        cart_data = self.get_cart(cart_id)
        if cart_data:
            if item_id in cart_data['items']:
                if action == 'add':
                    cart_data['items'][item_id]['quantity'] += 1
                elif action == 'remove':
                    if cart_data['items'][item_id]['quantity'] > 1:
                        cart_data['items'][item_id]['quantity'] -= 1
                    else:
                        del cart_data['items'][item_id]
            else:
                cart_data['items'][item_id] = {'quantity': 1}
            # Recalculate totals
            cart_data['subtotal'] = sum(item['price'] * item['quantity'] for item in cart_data['items'].values())
            cart_data['tax'] = cart_data['subtotal'] * 0.08  # Simulate 8% tax
            cart_data['shipping'] = 5  # Simulate flat shipping rate
            cart_data['total'] = cart_data['subtotal'] + cart_data['tax'] + cart_data['shipping']
            # Update cache
            self.cache[cart_id] = cart_data
            return cart_data
        return None

    def get_cart_data(self, cart_id):
        """Return cart data for given ID"""
        return self.cache.get(cart_id)


# Example usage:
cart = Cart()
cart_id = '12345'

# Initialize cart
cart_data = cart.get_cart(cart_id)
if cart_data:
    print(json.dumps(cart_data, indent=4))

# Add item to cart
cart_data = cart.update_cart(cart_id, 'item1', 'add')
if cart_data:
    print(json.dumps(cart_data, indent=4))

# Remove item from cart
cart_data = cart.update_cart(cart_id, 'item1', 'remove')
if cart_data:
    print(json.dumps(cart_data, indent=4))