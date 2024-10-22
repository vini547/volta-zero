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

# Streamlit session state for tracking login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar for navigation
st.sidebar.title("Navigation")
if not st.session_state.logged_in:
    option = st.sidebar.selectbox("Select an option", ["Login", "Register"])
else:
    option = st.sidebar.selectbox("Select a page", ["Home", "Profile", "Settings", "Logout"])

# Login page
if option == "Login":
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.experimental_rerun()  # Reload the page
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

# Pages available after login
if st.session_state.logged_in:
    if option == "Home":
        st.title("Home Page")
        st.write("Welcome to the Home Page!")
    
    elif option == "Profile":
        st.title("Profile Page")
        st.write("This is your Profile Page.")
    
    elif option == "Settings":
        st.title("Settings Page")
        st.write("Here you can adjust your settings.")

    elif option == "Logout":
        st.session_state.logged_in = False
        st.success("You have logged out.")
        st.experimental_rerun()  # Reload the page