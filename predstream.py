import streamlit as st
import pandas as pd
from plotly import graph_objs as go
import yfinance as yf
from matplotlib import pyplot as py 
# Import the predict function from the previous code block
from var_model import predict
from var_model import actual
tickers=("AAPL","MSFT","GOOG","AMZN","META")


# Set the title of the app
st.title("Future Stock Price Predictions")

# Add a short description
st.write("Enter a start and end date to get predictions.")

selected_stock = st.selectbox("Select stock for prediction",tickers)

# Add input fields for the start and end dates
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

# Add a button to make the predictions
if st.button("Get Predictions"):
    # Call the predict function with the input dates

    with st.container():
        st.write("---")
        left_col, right_col = st.columns((1,2))

        with left_col:
            predictions = predict(start_date, end_date)
            # Display the predicted values in a table
            actualdata= actual(start_date, end_date,selected_stock)
            st.write(predictions[selected_stock])

            ss = predictions[selected_stock]

        with right_col:
            def plot_raw_data():
                
                #df = pd.DataFrame()

                #for ticker in tickers:
                    #df[ticker] = data[ticker]['Close']

                #date1 = data['Date']
                #df = pd.concat([date1, df], axis=1)
                #df.to_csv('stocks.csv')
                #df = pd.read_csv('stocks.csv', parse_dates=['Date'], index_col='Date')
                fig = go.Figure()
                fig.add_trace(go.Scatter(x= predictions.index, y= ss, name="stock_open"))
                fig.add_trace(go.Scatter(x= actualdata.index, y= actualdata["Close"], name="actual"))
                fig.layout.update(title_text='Time Series data with Range slider', xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)
            plot_raw_data()