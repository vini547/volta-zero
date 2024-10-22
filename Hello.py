import streamlit as st

# In-memory user storage for demonstration purposes (you may want to use a database in production)
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

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Display Login/Register buttons
if not st.session_state.logged_in:
    st.title("Welcome to the App")
    
    # Buttons for Login and Register
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login", key="login_button"):
            st.session_state.page = "login"
    
    with col2:
        if st.button("Register", key="register_button"):
            st.session_state.page = "register"

# Handle Login and Registration
if st.session_state.get("page") == "login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login", key="login_submit"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.experimental_rerun()  # Reload the page
        else:
            st.error("Invalid username or password.")
    
elif st.session_state.get("page") == "register":
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    
    if st.button("Register", key="register_submit"):
        if register_user(new_username, new_password):
            st.success("Registration successful! You can now log in.")
            st.session_state.page = "login"  # Automatically switch back to login
        else:
            st.error("Username already exists. Please choose a different username.")

# Pages available after login
if st.session_state.logged_in:
    st.title("Home Page")
    st.write("Welcome to the Home Page!")
    st.write("You can access other pages in the 'pages' folder now.")

    if st.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.page = None  # Reset the page
        st.success("You have logged out.")
        st.experimental_rerun()  # Reload the page
