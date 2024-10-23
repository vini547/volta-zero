import streamlit as st
import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
DB_HOST = "your_postgres_host"
DB_NAME = "your_database_name"
DB_USER = "your_username"
DB_PASSWORD = "your_password"

# Function to create a connection to PostgreSQL
def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Function to register a new user
def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return "Username already exists."
    
    # Insert new user into the users table
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return "User registered successfully."

# Function to login a user
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the username and password match
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    stored_password = cursor.fetchone()
    
    if stored_password and stored_password[0] == password:
        st.session_state.logged_in = True
        return True
    
    cursor.close()
    conn.close()
    return False

# Initializing session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login/Register Page
if not st.session_state.logged_in:
    st.title("Login Page")
    
    menu = st.radio("Choose an option:", ["Login", "Register"])
    
    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.experimental_rerun()  # Rerun to refresh the app state
            else:
                st.error("Invalid username or password.")
    
    elif menu == "Register":
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        if st.button("Register"):
            message = register_user(username, password)
            st.success(message)

# Main app content accessible only when logged in
if st.session_state.logged_in:
    st.title("Welcome to the App!")
    st.write("You are now logged in.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
