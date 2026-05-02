import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

np.random.seed(42)
dates = pd.date_range(start='2021-01-01', end='2023-12-31', freq='M')
trend = np.linspace(100, 500, len(dates))
seasonality = 50 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
noise = np.random.normal(0, 20, len(dates))
sales = trend + seasonality + noise

df = pd.DataFrame({'Date': dates, 'Sales': sales})
df.set_index('Date', inplace=True)

decomposition = seasonal_decompose(df['Sales'], model='additive')
model = ExponentialSmoothing(df['Sales'], seasonal='add', seasonal_periods=12).fit()
forecast = model.forecast(12)

fig, axes = plt.subplots(4, 1, figsize=(12, 10))
decomposition.observed.plot(ax=axes[0], title='Observed')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonality')
forecast.plot(ax=axes[3], title='12-Month Forecast', color='red')
plt.tight_layout()
plt.show()