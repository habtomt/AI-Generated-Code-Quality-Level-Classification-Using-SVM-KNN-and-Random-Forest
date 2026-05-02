import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def sales_forecasting():
    dates = pd.date_range(start='2020-01-01', periods=36, freq='M')
    sales = [100 + i*2 + np.random.randint(-5, 5) for i in range(36)]
    df = pd.DataFrame({'Date': dates, 'Sales': sales})
    df.set_index('Date', inplace=True)
    
    model = ExponentialSmoothing(df['Sales'], trend='add', seasonal=None)
    model_fit = model.fit()
    forecast = model_fit.forecast(12)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Sales'], label='Historical Sales')
    plt.plot(pd.date_range(start=dates[-1], periods=12, freq='M'), forecast, label='Forecast', linestyle='--')
    plt.legend()
    plt.title('Sales Trend Prediction')
    plt.show()
    
    print(forecast)

if __name__ == "__main__":
    sales_forecasting()
