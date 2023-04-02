import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.api import VAR

tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

# Import data from Yahoo Finance and set group_by to 'ticker'
data = yf.download(tickers, start="2019-01-01", end="2023-03-01", group_by='ticker')

# Reset the index to add the date column as a separate column
data = data.reset_index()
df = pd.DataFrame()

for ticker in tickers:
    df[ticker] = data[ticker]['Close']

date1 = data['Date']
df = pd.concat([date1, df], axis=1)
df.to_csv('stocks.csv')
df = pd.read_csv('stocks.csv', parse_dates=['Date'], index_col='Date')

# Select the columns to use for forecasting
columns = ['AAPL', 'MSFT', 'GOOG', 'AMZN','META']
dataf = df[columns]

datastd=dataf
#scaler=StandardScaler()
#datastd=pd.DataFrame(scaler.fit_transform(dataf), columns=columns)


# Fit a VAR model to the data
model = VAR(datastd)
results = model.fit(400)

# Define a function to make predictions
def predict(start, end):
    # Create a date range based on the start and end dates
    date_range = pd.date_range(start=start, end=end)

    #datastd=pd.DataFrame(scaler.fit_transform(dataf), columns=columns)
    
    # Use the model to make predictions for the date range
    predictions = results.forecast(datastd.values[-results.k_ar:], len(date_range))

    #predictions = scaler.inverse_transform(predictions)
    # Convert the predictions to a DataFrame and set the column names
    preds_df = pd.DataFrame(predictions, index=date_range, columns=columns)

    # Return the predictions DataFrame
    return preds_df
def actual(start, end,tickers):
    r=yf.download(tickers,start=start, end=end)
    return r