import time
import math
import requests
import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.varmax import VARMAX
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PIL import Image as pl
import plotly.express as px
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_option_menu import option_menu
import plotly.graph_objs as go


def plot_in_full_percentage(df3, df4):
    ax18 = st.checkbox("Show Description",key="18")
    if ax18:    
        
        st.markdown("""Plot the In-Full Percentage over time using the data available in the datasets. The function displays this plot in the Streamlit app.

*Parameters:*
df3: Target of orders dataset dataframe, which contains target percentages for various delivery metrics.
df4: Order dataset dataframe, which contains details about the orders including whether they were delivered in full.""",True)
    # Calculate the average of 'infull_target%'
    average_infull_target = df3['infull_target%'].mean()

    # Convert the 'order_placement_date' column to datetime type
    df4['order_placement_date'] = pd.to_datetime(df4['order_placement_date'])

    # Extract the month and year from the 'order_placement_date' column
    df4['month_year'] = df4['order_placement_date'].dt.to_period('M').astype(str)  # Convert to string

    # Calculate the In-Full Percentage (IF%) based on the 'In Full' column
    df4['in_full_percentage'] = df4['In Full'] * 100

    # Group the data by 'month_year' and calculate the mean of 'in_full_percentage'
    monthly_in_full = df4.groupby('month_year')['in_full_percentage'].mean().reset_index()

    # Create an interactive line chart with hover tooltips for In-Full Percentage (IF%)
    fig = px.line(
        monthly_in_full,
        x='month_year',
        y='in_full_percentage',
        title='In-Full Percentage Over Time (Dynamic Ordering)',
        labels={'month_year': 'Month', 'in_full_percentage': 'In-Full Percentage (%)'},
        markers=True,
        line_shape='linear',
    )

    # Add a line for the average infull_target% from df3
    average_infull_target_line = go.Scatter(
        x=monthly_in_full['month_year'],
        y=[average_infull_target] * len(monthly_in_full),
        mode='lines',
        line=dict(dash='dash', color='red'),
        name="In-Full Target"
    )

    # Add a line for the blue line (IF%) with a legend
    in_percentage_line = go.Scatter(
        x=monthly_in_full['month_year'],
        y=monthly_in_full['in_full_percentage'],
        mode='lines',
        line=dict(color='blue'),
        name="In-Full Percentage (InFull%)"
    )

    fig.add_trace(average_infull_target_line)
    fig.add_trace(in_percentage_line) 

    # Display the plot using Streamlit
    st.plotly_chart(fig)

# Read in the data and call the function to display the plot on the Streamlit app

def plot_on_time_percentage(df3, df4):
    ax17 = st.checkbox("Show Description",key="17")
    if ax17:    
        
        st.markdown("""Plot the On-Time Percentage over time using the data available in the datasets. The function displays this plot in the Streamlit app.

*Parameters*:
df3: Target of orders dataset dataframe, which contains target percentages for various delivery metrics.
df4: Order dataset dataframe, which contains details about the orders including whether they were delivered on time.""",True)
    # Calculate the average of 'ontime_target%'
    average_ontime_target = df3['ontime_target%'].mean()

    # Convert the 'order_placement_date' column to datetime type
    df4['order_placement_date'] = pd.to_datetime(df4['order_placement_date'])

    # Extract the month and year from the 'order_placement_date' column
    df4['month_year'] = df4['order_placement_date'].dt.to_period('M').astype(str)  # Convert to string

    # Calculate the On-Time Percentage (OnTime%) based on the 'On Time' column
    df4['ontime_percentage'] = df4['On Time'] * 100

    # Group the data by 'month_year' and calculate the mean of 'ontime_percentage'
    monthly_ontime = df4.groupby('month_year')['ontime_percentage'].mean().reset_index()

    # Create an interactive line chart with hover tooltips for On-Time Percentage (OnTime%)
    fig = px.line(
        monthly_ontime,  # Use the DataFrame with 'month_year' and 'ontime_percentage'
        x='month_year',
        y='ontime_percentage',
        title='On-Time Percentage Over Time (Dynamic Ordering)',
        labels={'month_year': 'Month', 'ontime_percentage': 'On-Time Percentage (%)'},
        markers=True,
        line_shape='linear',
    )

    # Add a line for the average ontime_target% from df3
    fig.add_trace(go.Scatter(
        x=monthly_ontime['month_year'],
        y=[average_ontime_target] * len(monthly_ontime),
        mode='lines',
        line=dict(dash='dash', color='red'),
        name="On-Time Target"
    ))

    # Add legend for OnTime Percentage (OnTime%)
    fig.add_trace(go.Scatter(
        x=monthly_ontime['month_year'],
        y=monthly_ontime['ontime_percentage'],
        mode='lines',
        line=dict(color='blue'),
        name="On-Time Percentage (OnTime%)"
    ))

    # Display the plot using Streamlit
    st.plotly_chart(fig)

def visualize_otif(df3, df4):
    ax16 = st.checkbox("Show Description",key="16")
    if ax16:    
        
        st.markdown("""Visualize the On-Time In-Full (OTIF) Percentage over time using the data available in the datasets. The function displays this plot in the Streamlit app.

*Parameters*:
df3: Target of orders dataset dataframe, which contains target percentages for various delivery metrics.
df4: Order dataset dataframe, which contains details about the orders including whether they were delivered on time and in full.""",True)
    # Calculate the average of 'otif_target%'
    average_otif_target = df3['otif_target%'].mean()

    # Convert the 'order_placement_date' column to datetime type
    df4['order_placement_date'] = pd.to_datetime(df4['order_placement_date'])

    # Extract the month and year from the 'order_placement_date' column
    df4['month_year'] = df4['order_placement_date'].dt.to_period('M').astype(str)  # Convert to string

    # Calculate the On-Time In Full Percentage (OnTime In Full%) based on the 'On Time In Full' column
    df4['ontime_in_full_percentage'] = df4['On Time In Full'] * 100

    # Group the data by 'month_year' and calculate the mean of 'ontime_in_full_percentage'
    monthly_ontime_in_full = df4.groupby('month_year')['ontime_in_full_percentage'].mean().reset_index()

    # Create an interactive line chart with hover tooltips for On-Time In Full Percentage (OnTime In Full%)
    fig = px.line(
        monthly_ontime_in_full,  # Use the DataFrame with 'month_year' and 'ontime_in_full_percentage'
        x='month_year',
        y='ontime_in_full_percentage',
        title='On-Time In Full Percentage Over Time (Dynamic Ordering)',
        labels={'month_year': 'Month', 'ontime_in_full_percentage': 'On-Time In Full Percentage (%)'},
        markers=True,
        line_shape='linear',
    )

    # Add a line for the average otif_target% from df3 with legend
    fig.add_trace(go.Scatter(
        x=monthly_ontime_in_full['month_year'],
        y=[average_otif_target] * len(monthly_ontime_in_full),
        mode='lines',
        line=dict(dash='dash', color='red'),
        name="OTIF Target"
    ))

    # Add legend for OnTime In Full Percentage (OnTime In Full%)
    fig.add_trace(go.Scatter(
        x=monthly_ontime_in_full['month_year'],
        y=monthly_ontime_in_full['ontime_in_full_percentage'],
        mode='lines',
        line=dict(color='blue'),
        name="On-Time In Full Percentage (OnTime In Full%)"
    ))

    # Use Streamlit to display the Plotly figure
    st.plotly_chart(fig)

def calculate_metrics(d4, d3):
    ax15 = st.checkbox("Show Description",key="15")
    if ax15:    
        
        st.markdown("""Calculate various supply chain metrics including On-Time Percentage, In-Full Percentage, and On-Time In-Full Percentage, along with their respective target values from the target of orders dataset. The function returns these metrics in a dictionary.

*Parameters*:
df4: Order dataset dataframe, which contains details about the orders including whether they were delivered on time and in full.
df3: Target of orders dataset dataframe, which contains target percentages for various delivery metrics.
*Returns*:
A dictionary containing the calculated metrics and their respective values.
""",True)

    # Calculate metrics
    ontime_percent = d4['On Time'].sum() / len(d4) * 100
    in_full_percent = d4['In Full'].sum() / len(d4) * 100
    ontime_in_full_percent = d4['On Time In Full'].sum() / len(d4) * 100
    
    # Merge order data with target data to get target values for each order
    merged_data = d4.merge(d3, on="customer_id", how="left")
    
    # Calculate target metrics
    target_on_time = merged_data['ontime_target%'].mean()
    target_in_full = merged_data['infull_target%'].mean()
    target_ontime_in_full = merged_data['otif_target%'].mean()

    # Create a dictionary to hold the results
    results = {
        'OnTime%': ontime_percent,
        'Target On Time': target_on_time,
        'In Full%': in_full_percent,
        'Target In Full': target_in_full,
        'OnTime In Full%': ontime_in_full_percent,
        'Target OnTime In Full': target_ontime_in_full,
    }
    
    return results
def visualize_days_delay(df):
    # Remove parentheses and commas from date columns
    df['agreed_delivery_date'] = df['agreed_delivery_date'].str.replace("(", "").str.replace(")", "").str.replace(",", "")
    df['actual_delivery_date'] = df['actual_delivery_date'].str.replace("(", "").str.replace(")", "").str.replace(",", "")

    # Define the date format based on your cleaned date columns
    date_format = "%A %B %d %Y"

    # Use to_datetime with the specified format
    df['agreed_delivery_date'] = pd.to_datetime(df['agreed_delivery_date'], format=date_format)
    df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'], format=date_format)

    # Calculate the day delay and store it in a new column
    df['day_delay'] = (df['actual_delivery_date'] - df['agreed_delivery_date']).dt.days

    # Calculate the total orders for each day delay
    total_orders = df.groupby('day_delay').size().reset_index(name='total_orders')

    # Create a stacked bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(total_orders['day_delay'], total_orders['total_orders'], color='red', label='On Time')
    plt.xlabel('Day Delay')
    plt.ylabel('Total Orders')
    plt.title('Total Orders by Day Delay')
    plt.legend()
    st.pyplot(plt)  # Display the chart in Streamlit
