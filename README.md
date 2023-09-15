# Supply Sage - Mastering the Chain, Predicting the Gain!

Supply Sage is your one-stop solution for analyzing and forecasting the supply chain data of companies. Leverage the powerful capabilities of data analytics to master the supply chain and predict gains more efficiently. Simplify and streamline your supply chain analysis with our easy-to-use web platform built with Streamlit, Python, and MySQL.

## Features

### 📊 Upload Data

- Upload various datasets in CSV format.
- View samples of each dataset to understand the expected format of the files.

### 📈 Supply Chain Analysis

- Verify and evaluate your current supply chain performance.
- Interpret and visualize different metrics and trends over time.

### 📉 Demand Forecasting

- Forecast the demand for various products for a period ranging from 1 to 30 days.
- Get average forecasted demand for selected products.


## Development Setup

Ensure you have Python 3.8+ and MySQL installed.

### Database Setup

Before running the application, you need to set up the database with the necessary tables. Open your MySQL console or a MySQL management tool like MySQL Workbench and run the following SQL query to create the users table:

```sql
CREATE DATABASE IF NOT EXISTS supply_sage_db;

USE supplychain;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
sh
Copy code
# Clone the repository
git clone https://github.com/tarun-kt-codes/Supply-Sage.git

# Change directory
cd supply-sage

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

Contributing
We welcome contributions! Please see our contributing guide for more details.

Contact
For any questions, feel free to reach out to us at: https://www.linkedin.com/in/tarun-k-t-4860b721a/

Acknowledgements
Streamlit
Python
MySQL


