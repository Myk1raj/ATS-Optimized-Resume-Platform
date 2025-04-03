import streamlit as st
import requests
from components.header import show_header

def render_page():
    show_header()
    st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>LOGIN / SIGN UP</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.form_submit_button("Login", use_container_width=True):
                if email and password:
                    st.session_state.user = email
                    st.session_state.page = 'upload'
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

    with tab2:
        with st.form("signup_form"):
            name = st.text_input("Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            if st.form_submit_button("Sign Up", use_container_width=True):
                if name and email and password:
                    st.session_state.user = email
                    st.session_state.page = 'upload'
                    st.rerun()
                else:
                    st.error("Please fill in all fields")