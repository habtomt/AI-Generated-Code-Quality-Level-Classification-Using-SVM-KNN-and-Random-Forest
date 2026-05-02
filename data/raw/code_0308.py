"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_001.txt
Run      : 1
"""

import hashlib
import time
from enum import Enum
from typing import Dict, List

# Define the supply chain states
class State(Enum):
    Manufactured = 1
    InTransit = 2
    Delivered = 3

# Define a product class
class Product:
    def __init__(self, id: int, name: str, manufacturer: str):
        self.id = id
        self.name = name
        self.manufacturer = manufacturer
        self.state = State.Manufactured
        self.history = [(State.Manufactured, int(time.time()))]

    def ship(self):
        if self.state == State.Manufactured:
            self.state = State.InTransit
            self.history.append((State.InTransit, int(time.time())))
        else:
            raise ValueError("Product is not ready to ship")

    def deliver(self):
        if self.state == State.InTransit:
            self.state = State.Delivered
            self.history.append((State.Delivered, int(time.time())))
        else:
            raise ValueError("Product is not in transit")

    def verify(self):
        return self.name, self.manufacturer, self.state

# Define a supply chain class
class SupplyChain:
    def __init__(self):
        self.products: Dict[int, Product] = {}
        self.product_count = 0

    def create_product(self, name: str, manufacturer: str):
        self.product_count += 1
        self.products[self.product_count] = Product(self.product_count, name, manufacturer)

    def get_product(self, product_id: int):
        if product_id in self.products:
            return self.products[product_id]
        else:
            raise ValueError("Invalid product ID")

    def ship_product(self, product_id: int):
        product = self.get_product(product_id)
        try:
            product.ship()
        except ValueError as e:
            print(f"Error shipping product {product_id}: {e}")

    def deliver_product(self, product_id: int):
        product = self.get_product(product_id)
        try:
            product.deliver()
        except ValueError as e:
            print(f"Error delivering product {product_id}: {e}")

    def verify_product(self, product_id: int):
        product = self.get_product(product_id)
        return product.verify()

# Test the supply chain
try:
    chain = SupplyChain()
    chain.create_product("Test Product", "Test Manufacturer")
    print(chain.verify_product(1))  # Verify product details
    chain.ship_product(1)
    print(chain.verify_product(1))  # Verify product details after shipping
    chain.deliver_product(1)
    print(chain.verify_product(1))  # Verify product details after delivery
except Exception as e:
    print(f"Error: {e}")