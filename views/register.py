import streamlit as st
import time
from utils import authenticate
from models import account

def show():
    # Custom CSS for improved UI
    page_style = """
    <style>
    /* Centering the form */
    .register-container {
        max-width: 400px;
        margin: auto;
        padding: 40px;
        background-color: #1f1f1f;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        position: relative;
        top: 50%;
        transform: translateY(-50%);
    }

    .register-header {
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #f0f0f0;
        margin-bottom: 30px;
        font-size: 24px;
    }

    /* Styling the inputs */
    input {
        color: #f0f0f0 !important;
        background-color: #2c2c2c !important;
        border: 1px solid #555 !important;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        width: 100%;
    }

    /* Styling the buttons */
    div.stButton > button {
        width: 100%;
        background-color: #28a745;
        color: white;
        padding: 10px;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 15px;
        font-family: 'Arial', sans-serif;
    }

    div.stButton > button:hover {
        background-color: #218838;
    }

    div.stButton > button.secondary-btn {
        background-color: #6c757d;
        margin-top: 10px;
    }

    div.stButton > button.secondary-btn:hover {
        background-color: #5a6268;
    }
    </style>
    """

    # Apply CSS
    st.markdown(page_style, unsafe_allow_html=True)

    # Form layout container
    st.markdown('<div class="register-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="register-header">Đăng ký tài khoản</h2>', unsafe_allow_html=True)

    # User input field
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type='password')
    confirmPassword = st.text_input("Nhập lại mật khẩu", type='password')

    if st.button("Đăng ký"):
        if authenticate.check_register(username, password, confirmPassword):
            account.add_account(username, password)
            st.success("Đăng ký thành công!")
            st.session_state.page = "Login"  
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Vui lòng kiểm tra lại thông tin đăng ký.")
            time.sleep(1.5)
            st.rerun()

    if st.button("Trở lại đăng nhập", key="back_to_login"):
        st.session_state.page = "Login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
