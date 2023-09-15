import streamlit as st
import mysql.connector 
from hashlib import sha256
from PIL import Image as pl
import base64
import io



with open('styles.css', 'r') as f:
    css = f.read()

# Apply the CSS styles using st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Specify the new size
new_width = 300
new_height = 300

# Open the image using PIL
str_path = "C:\\Users\HP\\Documents\\Supply Sage\\Images\\logo.PNG"
img = pl.open(str_path)

# Get the original size of the image
width, height = img.size

# Calculate the ratio to maintain the aspect ratio
ratio = min(new_width/width, new_height/height)

# Calculate the new size maintaining the aspect ratio
new_width = int(width * ratio)
new_height = int(height * ratio)

# Resize the image
img = img.resize((new_width, new_height), pl.ANTIALIAS)

# Now you can use this resized image in your Streamlit app


buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

st.markdown(
    f'<img src="data:image/png;base64,{img_str}" style="display: block; margin: auto;" />',
    unsafe_allow_html=True,
)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tarunsql123",
    database="supplychain"
)
cursor = db.cursor()

# Streamlit login page
st.markdown(
    f'<h1 style="color: #e32400;">Login Page</h1>',
    unsafe_allow_html=True,
)


menu = ["Login", "Signup"]
choice = st.selectbox("Select Option", menu)

if choice == "Login":
    st.markdown(
    f'<h2 style="color: #e32400;">Login</h2>',
    unsafe_allow_html=True,
)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        hashed_password = sha256(password.encode()).hexdigest()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        if user:
            st.success("Logged in as: {}".format(username))
    
    # Clear login page content
            st.empty()
    
    # Display a link to redirect to the new welcome webpage
            
            redirect_url = "http://localhost:8502"  # The URL to redirect to
            st.markdown(
            f'<meta http-equiv="refresh" content="0;url={redirect_url}">', 
    unsafe_allow_html=True,
)
        else:
            st.error("Invalid username or password")


if choice == "Signup":
    st.markdown(
    f'<h2 style="color: #e32400;">Create an Account</h2>',
    unsafe_allow_html=True,
)

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Signup"):
        # Check if the username already exists
        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (new_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        else:
            hashed_password = sha256(new_password.encode()).hexdigest()
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (new_username, hashed_password))
            db.commit()
            st.success("Account created successfully! You can now log in.")

# Don't forget to close the database connection
db.close()