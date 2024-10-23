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
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    return users

# Function for user registration
def register_user(username, password):
    users = read_users()
    if username in users:
        return "Username already exists."
    
    with open(CREDENTIALS_FILE, 'a') as file:
        file.write(f"{username},{password}\n")
    
    return "User registered successfully."

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
    st.experimental_set_query_params(logged_in="false")  # Clear login state

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
                st.experimental_set_query_params(logged_in="true")  # Trigger a rerun
            else:
                st.error("Invalid username or password.")
    
    elif menu == "Register":
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        if st.button("Register", key="register_button"):
            message = register_user(username, password)
            st.success(message)

# Main app content accessible only when logged in
if st.session_state.logged_in:
    st.title("Welcome to the App!")
    st.write("You are now logged in.")
    
    # Log Out Button
    if st.button("Log Out", key="logout_button"):
        logout_user()
        st.experimental_rerun()  # This will rerun the app and take the user back to the login page