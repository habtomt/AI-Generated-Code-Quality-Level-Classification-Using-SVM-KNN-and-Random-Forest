import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

prices = np.array([10, 15, 20, 25, 30, 35, 40, 45, 50]).reshape(-1, 1)
demand = np.array([500, 440, 380, 310, 250, 190, 130, 80, 40])

model = LinearRegression().fit(prices, demand)

sim_prices = np.linspace(10, 60, 50).reshape(-1, 1)
pred_demand = model.predict(sim_prices)
pred_revenue = sim_prices.flatten() * pred_demand

opt_price = sim_prices[np.argmax(pred_revenue)][0]

plt.figure(figsize=(10, 5))
plt.plot(sim_prices, pred_revenue, label='Revenue')
plt.axvline(opt_price, color='r', linestyle='--', label=f'Optimal Price: {opt_price:.2f}')
plt.legend()
plt.show()

print(f"Optimal Price: {opt_price}")