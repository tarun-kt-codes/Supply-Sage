import time
import os
import math
import requests
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PIL import Image as pl
import plotly.express as px
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_option_menu import option_menu
import plotly.graph_objs as go
import DemandForecasting as demf
import SupplyChainAnalysis as sca


with open('styles.css', 'r') as f:
    css = f.read()



plt.style.use("ggplot")

st.set_option('deprecation.showPyplotGlobalUse', False) 

def loadlottieurl(url:str):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

lottie_url_teach = 'https://assets3.lottiefiles.com/packages/lf20_22mjkcbb.json'
lottie_url_inspect = 'https://assets6.lottiefiles.com/packages/lf20_49rdyysj.json'


lottie_stat = loadlottieurl(lottie_url_inspect)
lottie_teach = loadlottieurl(lottie_url_teach)
head,anim=st.columns(2)

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

styled_text = """
    <h1 style='color: white;'><i>Supply Sage</i></h1>
"""

with head:
        st.write(" ")
        st.write(" ")

        # Get the current directory of the script
        current_dir = os.path.dirname(__file__)
        
        # Construct the file path dynamically
        image_filename = "logo.PNG"
        image_path = os.path.join(current_dir, image_filename)

        st.image(img, width=300)

with anim:
    st_lottie(lottie_stat,key='stat', width=300, height=300)

with st.sidebar:
    sel=option_menu(
        menu_title='Main Menu',
        options=['Home','Upload Data','Supply Chain Analysis','Demand Forecasting'],
        icons=['house','table','activity','graph-up-arrow']        
    )
if sel == 'Home':
# Your Home page content here
    st.markdown("""
        ## Welcome to Supply Sage! 
        
        Supply Sage is your one-stop solution for analyzing and forecasting the supply chain data of companies. Leverage the power of data analytics to master the supply chain and predict the gains efficiently. Here's what you can do with Supply Sage:""" , True)
        
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("""
        <div style="border: 2px solid #0e3b6e; border-radius: 5px; padding: 20px; background-color: #0e3b6e;">
            <h3 style="color: #ffffff;">📊 Upload Data</h3>
            <ul style="color: #ffffff;">
                <li>Upload various datasets in CSV format.</li>
                <li>View samples of each dataset to understand the expected format of the files.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border: 2px solid #0e3b6e; border-radius: 5px; padding: 20px; background-color: #0e3b6e;">
            <h3 style="color: #ffffff;">📈 Supply Chain Analysis</h3>
            <ul style="color: #ffffff;">
                <li>Verify and evaluate your current supply chain performance.</li>
                <li>Interpret &</li>
                <li>Visualize the different metrics and the trends over time.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="border: 2px solid #0e3b6e; border-radius: 5px; padding: 20px; background-color: #0e3b6e;">
            <h3 style="color: #ffffff;">📉 Demand Forecasting</h3>
            <ul style="color: #ffffff;">
                <li>Forecast the demand for various products for a period ranging from 1 to 30 days.</li>
                <li>Get average forecasted demand for selected products.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    
    st.markdown("""
        ### Let's get started! Choose an option from the main menu to proceed. 
    """, True)

if sel=='Upload Data':
    st.markdown("""
        ### Upload the Required Datasets 
        
        Here, you can upload four different datasets that are essential for the supply chain analysis and demand forecasting. Below, we have described each dataset and what all features they should contain""")
    st.markdown("""#### *1. Customer Dataset*""")
    ax11 = st.checkbox("Show Description",key="11")
    if ax11:    
        
        st.markdown("""This dataset contains information about the customers. It is used to identify and analyze the details related to individual customers in your business.
            
            - *customer_id:* A unique identifier for each customer.
            - *customer_name:* The name of the customer.
            - *city:* The city where the customer is located.
        """,True)
    uploaded_file1 = st.file_uploader("Upload the Customer Dataset CSV file", type="csv")
    if uploaded_file1 is not None:
        df1 = pd.read_csv(uploaded_file1)
        st.session_state.df1 = df1
    ax1 = st.checkbox("Show sample Customer dataset",key="1")
    if ax1:
        str_path = "C:\\Users\HP\\Documents\\Supply Sage\\Images\\cust.PNG"
        img = pl.open(str_path)
        st.image(img, width=350)

    st.markdown("""#### *2. Product Dataset*""")
    ax12 = st.checkbox("Show Description",key="12")
    if ax12:    
        
        st.markdown("""This dataset houses details about the products that your company offers. It includes identifiers and the categories of the products.
        
        - *product_name:* The name of the product.
        - *product_id:* A unique identifier for each product.
        - *category:* The category to which the product belongs.""",True)
    uploaded_file2 = st.file_uploader("Upload the Product Dataset CSV file", type="csv")
    if uploaded_file2 is not None:
        df2 = pd.read_csv(uploaded_file2)
        st.session_state.df2 = df2  
    ax2 = st.checkbox("Show sample Product dataset",key="2")
    if ax2:
        str_path = "C:\\Users\HP\\Documents\\Supply Sage\\Images\\prod.PNG"
        img = pl.open(str_path)
        st.image(img, width=350)

    st.markdown("""#### *3. Target of Orders Dataset*""")
    ax13 = st.checkbox("Show Description",key="13")
    if ax13:    
        
        st.markdown("""This dataset outlines the targets set for various delivery metrics. It helps in setting and tracking the goals for on-time and in-full deliveries.
        
        - *customer_id:* A unique identifier for each customer.
        - *ontime_target%:* The target percentage of on-time deliveries.
        - *infull_target%:* The target percentage of in-full deliveries.
        - *otif_target%:* The target percentage of on-time in-full deliveries.""",True)

    uploaded_file3 = st.file_uploader("Upload the Target of Order Dataset CSV file", type="csv")
    if uploaded_file3 is not None:
        df3 = pd.read_csv(uploaded_file3)
        st.session_state.df3 = df3  
    ax3 = st.checkbox("Show sample Target of Order dataset",key="3")
    if ax3:
        str_path = "C:\\Users\HP\\Documents\\Supply Sage\\Images\\targ.PNG"
        img = pl.open(str_path)
        st.image(img, width=350)

    st.markdown("""#### *4. Order Dataset*""")
    ax14 = st.checkbox("Show Description",key="14")
    if ax14:    
        
        st.markdown("""The order dataset encompasses all the details regarding the orders placed by customers, including the quantities ordered and delivered, and the delivery timelines.
        
        - *order_id:* A unique identifier for each order.
        - *order_placement_date:* The date when the order was placed.
        - *customer_id:* A unique identifier for each customer.
        - *product_id:* A unique identifier for each product.
        - *order_qty:* The quantity of products ordered.
        - *agreed_delivery_date:* The agreed date for the delivery of the order.
        - *actual_delivery_date:* The actual date when the delivery was made.
        - *delivery_qty:* The quantity of products delivered.
        - *In Full:* Whether the order was delivered in full or not (Yes/No).
        - *On Time:* Whether the order was delivered on time or not (Yes/No).
        - *On Time In Full:* Whether the order was delivered on time and in full or not (Yes/No).""",True)

    uploaded_file4 = st.file_uploader("Upload the Order Dataset CSV file", type="csv")
    if uploaded_file4 is not None:
        df4 = pd.read_csv(uploaded_file4)
        st.session_state.df4 = df4  
    ax4 = st.checkbox("Show sample Order dataset",key="4")
    if ax4:
        str_path = "C:\\Users\HP\\Documents\\Supply Sage\\Images\\ord.PNG"
        img = pl.open(str_path)
        st.image(img, width=1000)


if sel=="Supply Chain Analysis":
    warn="Please upload all the Dataset CSV file before proceeding."
    st.markdown("""
    ### Evaluating the performance of current supply chain of the company  
    """,True)
    
    op=st.selectbox("Choose an Analysis",['Key Performance Indicators','In-Full Percentage Over Time','On-Time Percentage Over Time','On-Time In-Full Percentage Over Time'])
  

    if(op=='Key Performance Indicators'):

        st.markdown("""Key Performance Indicators""")
        # Try to access df1,df2,df3,df4 from the session state
        if ('df3' in st.session_state) & ('df4' in st.session_state):
            # Get the results
            metrics=sca.calculate_metrics(st.session_state.df4,st.session_state.df3)

            # Display the results in Streamlit
            metrics_to_display = [
                ("OnTime%", "Target On Time"),
                ("In Full%", "Target In Full"),
                ("OnTime In Full%", "Target OnTime In Full"),
            ]

            for metric, target_metric in metrics_to_display:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.metric(label=metric, value=f"{metrics[metric]:.2f} %")
                
                with col2:
                    st.metric(label=target_metric, value=f"{metrics[target_metric]:.2f} %")
    


    if(op=='In-Full Percentage Over Time'):    
        st.markdown("""In-Full Percentage Over Time""")
        # Try to access df1,df2,df3,df4 from the session state
        if ('df3' in st.session_state) & ('df4' in st.session_state):
            sca.plot_in_full_percentage(st.session_state.df3,st.session_state.df4)
        else:
            st.warning(warn)

    if(op=='On-Time Percentage Over Time'):
        st.markdown("""On-Time Percentage Over Time""")
        # Try to access df1,df2,df3,df4 from the session state
        if ('df3' in st.session_state) & ('df4' in st.session_state):
            sca.plot_on_time_percentage(st.session_state.df3,st.session_state.df4)
        else:
            st.warning(warn)
    
    if(op=='On-Time In-Full Percentage Over Time'):
        st.markdown("""On-Time Percentage Over Time""")
        # Try to access df1,df2,df3,df4 from the session state
        if ('df3' in st.session_state) & ('df4' in st.session_state):
            sca.visualize_otif(st.session_state.df3,st.session_state.df4)
        else:
            st.warning(warn)


if sel=='Demand Forecasting':
    st.title('Product Demand Forecast')
    ax20 = st.checkbox("Show Description",key="20")
    if ax20:    
        
        st.markdown("""Forecast the demand for various products for a period ranging from 1 to 30 days.
        - Get average forecasted demand for selected products to aid in planning and inventory management.""",True)
# Try to access df4 from the session state
    if ('df4' in st.session_state) & ('df2' in st.session_state):
        # Streamlit UI
        
        product_name_option = st.selectbox('Select Product', st.session_state.df2['product_name'].unique())
        steps_option = st.number_input('Enter number of days for forecasting', min_value=1, max_value=365, value=30)

        if st.button('Get Forecast'):
            forecast_series,average_demand_forecast = demf.forecast_demand(st.session_state.df4, st.session_state.df2, product_name_option, steps_option)
            # Adding a line chart to visualize forecast data
            st.line_chart(forecast_series)

            # Displaying key metrics
            st.markdown("""#### *Average Forecasted Demand*""")
            st.metric(" ",f"{average_demand_forecast:.2f} units")
            #st.write(f'The average forecasted demand for {product_name_option} over the next {steps_option} days is {average_demand_forecast:.2f} units.')
    else:
        st.warning("Please upload the Product and Order Datasets CSV file before proceeding.")
