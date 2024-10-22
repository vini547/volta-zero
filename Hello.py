import streamlit as st

# User registration and login logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'users' not in st.session_state:
    st.session_state.users = {}

# Function for user registration
def register_user(username, password):
    if username in st.session_state.users:
        return "Username already exists."
    st.session_state.users[username] = password
    return "User registered successfully."

# Function for user login
def login_user(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        return True
    return False

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
                st.experimental_rerun()
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
    # Add content for logged-in users here
