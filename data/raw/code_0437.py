"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import tkinter as tk
from tkinter import ttk
import requests
import json

# Set up the API endpoint and credentials
API_ENDPOINT = "http://localhost:5000/products"
API_KEY = "YOUR_API_KEY"

class ProductUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Details")

        # Create a frame for product information
        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(fill="both", expand=True)

        # Create a label to display product image
        self.image_label = ttk.Label(self.info_frame)
        self.image_label.pack(fill="x")

        # Create a label to display product name
        self.name_label = ttk.Label(self.info_frame, text="")
        self.name_label.pack(fill="x")

        # Create a label to display product price
        self.price_label = ttk.Label(self.info_frame, text="")
        self.price_label.pack(fill="x")

        # Create a label to display product description
        self.description_label = ttk.Label(self.info_frame, text="", wraplength=400)
        self.description_label.pack(fill="both", expand=True)

        # Create a button to load additional product details
        self.load_button = ttk.Button(self.info_frame, text="Load Details", command=self.load_details)
        self.load_button.pack(fill="x")

        # Initialize the product ID
        self.product_id = None

    def load_product(self, product_id):
        try:
            # Make a GET request to fetch product details
            response = requests.get(f"{API_ENDPOINT}/{product_id}", headers={"Authorization": f"Bearer {API_KEY}"})

            # Check if the response was successful
            if response.status_code == 200:
                # Parse the response JSON
                product = response.json()

                # Update the product image
                self.image_label.config(image=tk.PhotoImage(file=product["image_url"]))

                # Update the product name
                self.name_label.config(text=product["name"])

                # Update the product price
                self.price_label.config(text=f"Price: ${product['price']}")

                # Update the product description
                self.description_label.config(text=product["description"])

                # Store the product ID for later use
                self.product_id = product_id
            else:
                print(f"Error fetching product: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product: {e}")

    def load_details(self):
        try:
            # Make a GET request to fetch additional product details
            response = requests.get(f"{API_ENDPOINT}/{self.product_id}/details", headers={"Authorization": f"Bearer {API_KEY}"})

            # Check if the response was successful
            if response.status_code == 200:
                # Parse the response JSON
                details = response.json()

                # Update the product description with additional details
                self.description_label.config(text=f"{self.description_label.cget('text')}\n\nAdditional Details:\n{details['details']}")
            else:
                print(f"Error fetching product details: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product details: {e}")

# Create the main window
root = tk.Tk()

# Create an instance of the ProductUI class
product_ui = ProductUI(root)

# Load a product with ID 1
product_ui.load_product(1)

# Start the Tkinter event loop
root.mainloop()