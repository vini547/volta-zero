import streamlit as st
import os

# File path for storing user credentials
CREDENTIALS_FILE = "users.txt"

# User registration and login logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to read users from the credentials file
def read_users():
    users = {}
    # Ensure the file exists before trying to read it
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    username, password = line.split(',')
                    users[username] = password
    return users

# Function for user registration
def register_user(username, password):
    users = read_users()
    if username in users:
        return "Username already exists."
    
    try:
        # Open the file in append mode and write the new user's credentials
        with open(CREDENTIALS_FILE, 'a') as file:
            file.write(f"{username},{password}\n")
        return "User registered successfully."
    except Exception as e:
        return f"Failed to register user: {e}"

# Function for user login
def login_user(username, password):
    users = read_users()
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        return True
    return False

# Function for logging out
def logout_user():
    st.session_state.logged_in = False
    st.experimental_set_query_params()  # Clear query parameters to refresh

# Login/Register Page
if not st.session_state.logged_in:
    st.title("Login Page")

    menu = st.radio("Choose an option:", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", key="login_button"):
            if login_user(username, password):
                st.success("Login successful!")
                st.experimental_set_query_params(logged_in="true")  # Force rerun with query params
            else:
                st.error("Invalid username or password.")
    
    elif menu == "Register":
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        if st.button("Register", key="register_button"):
            message = register_user(username, password)
            if "successfully" in message:
                st.success(message)
            else:
                st.error(message)

# Main app content accessible only when logged in
if st.session_state.logged_in:
    st.title("Welcome to the App!")
    st.write("You are now logged in.")
    
    # Log Out Button
    if st.button("Log Out", key="logout_button"):
        logout_user()
        st.experimental_set_query_params(logged_in="false")  # Reset query params to force rerun
