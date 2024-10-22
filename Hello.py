import streamlit as st
# In-memory user storage
users = {}

def register_user(username, password):
    """Register a new user."""
    if username in users:
        return False  # User already exists
    users[username] = password
    return True

def login_user(username, password):
    """Login the user."""
    return users.get(username) == password

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Select an option", ["Login", "Register"])

# Login page
if option == "Login":
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login_user(username, password):
            st.success("Login successful!")
            st.write(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

# Registration page
elif option == "Register":
    st.title("Registration Page")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    
    if st.button("Register"):
        if register_user(new_username, new_password):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Username already exists. Please choose a different username.")

# Optional: Display a logout button
if st.button("Logout"):
    st.success("You have logged out.")