import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta 

def forecast_demand(d4, d2, product_name, steps):
    # Convert the order placement date column to datetime
    d4['order_placement_date'] = pd.to_datetime(d4['order_placement_date'])
    
    # Group the data by product ID and date to find the total demand for each day
    daily_demand = d4.groupby(['product_id', 'order_placement_date'])['order_qty'].sum().reset_index()
    
    # Merge the daily_demand dataframe with the d2 dataframe to get the product names
    daily_demand = daily_demand.merge(d2[['product_id', 'product_name']], on='product_id', how='left')
    
    # Get the data for the selected product
    product_data = daily_demand[daily_demand['product_name'] == product_name]

    # Set the date as the index for time series analysis and specify the frequency as 'D' (daily)
    product_data.set_index('order_placement_date', inplace=True)
    product_data.index = pd.DatetimeIndex(product_data.index).to_period('D')

    # Fit ARIMA model (adjust p,d,q values as necessary)
    model = ARIMA(product_data['order_qty'], order=(5,1,0))
    model_fit = model.fit()
    
    # Forecast the next 'steps' days
    forecast = model_fit.get_forecast(steps=steps).predicted_mean

    forecast.index = forecast.index.to_timestamp()

    # Get the average forecasted demand
    average_forecast = forecast.mean()

    return forecast,average_forecast