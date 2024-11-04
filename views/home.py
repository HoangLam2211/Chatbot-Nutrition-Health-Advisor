import streamlit as st
import time
from views import chat, model, geo, visualization, brand

def show():
    st.sidebar.title("Home")
    page = st.sidebar.selectbox("Chọn tiện ích", 
                                ("Chatbot","Dự đoán", "Trực quan hóa địa lý", "Visualization"))
    if page == "Chatbot":
        chat.show()
    elif page == "Trực quan hóa địa lý":
        geo.app()
    elif page == "Dự đoán":
        model.show()
    elif page == "Visualization":
        visualization.show()
 

    