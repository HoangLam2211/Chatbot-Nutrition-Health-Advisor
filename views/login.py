import streamlit as st
import time
from utils import authenticate

def show():

    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    # button_style = """
    #     <style>
    #     div.stButton > button {
    #     width : 100%;
    #     border-radius: 10px;
    # }

    # div.stButton > button:hover {
    #     width : 100%;
    # }
    #     </style>
    # """

    button_style = """
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 50px;
            background-color: #f9f9f9;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .login-header {
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #333;
            margin-bottom: 20px;
        }
        div.stButton > button {
            width : 100%;
            background-color: #007bff;
            color: white;
            padding: 10px 0;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Arial', sans-serif;
            margin-bottom: 10px;
        }
        div.stButton > button:hover {
            background-color: #0056b3;
            color: white;
        }
        div.stButton > button.register-btn {
            background-color: #28a745;
        }
        div.stButton > button.register-btn:hover {
            background-color: #218838;
        }
        </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)
    if st.button("Login"):
        if authenticate.check_login(username, password):
            st.success("Login successful!")
            st.session_state.page = "Home" 
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Fail.")
            time.sleep(0.5)
            st.rerun()
    
    if st.button("Register"):
        st.session_state.page = "Register"
        st.rerun()