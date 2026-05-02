"""
Auto-generated Python code
Scenario : Data Analysis
Prompt   : response_003.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Sample dataset (replace with your actual data)
# Assuming we have the following columns: 'Price', 'Demand', 'Revenue'
data = {
    'Price': np.random.uniform(10, 50, 100),
    'Demand': np.random.uniform(100, 500, 100),
    'Revenue': np.random.uniform(1000, 5000, 100)
}
df = pd.DataFrame(data)

# Define features (X) and target (y)
X = df[['Price']]
y = df['Revenue']

# Scale the data using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model using mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Define a function to predict revenue based on price
def predict_revenue(price):
    price_scaled = scaler.transform([[price]])
    return model.predict(price_scaled)[0]

# Example usage: predict revenue for a price of $30
predicted_revenue = predict_revenue(30)
print(f'Predicted Revenue for Price $30: ${predicted_revenue:.2f}')

# Dynamic pricing strategy: adjust price to maximize revenue
def dynamic_pricing_strategy(price, target_revenue):
    while True:
        predicted_revenue = predict_revenue(price)
        if predicted_revenue >= target_revenue:
            print(f'Optimal Price: ${price:.2f}, Predicted Revenue: ${predicted_revenue:.2f}')
            break
        else:
            price += 0.1  # increment price by $0.10

# Example usage: find the optimal price to reach a target revenue of $2500
dynamic_pricing_strategy(10, 2500)