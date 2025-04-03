# frontend/session.py
import streamlit as st

def initialize_session():
    """Initialize session state variables if they don't exist"""
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'processed_resume' not in st.session_state:
        st.session_state.processed_resume = None
    if 'original_resume' not in st.session_state:
        st.session_state.original_resume = None

def set_page(page_name):
    """Navigate to specified page"""
    st.session_state.page = page_name
    
def login_user(email):
    """Set logged in user"""
    st.session_state.user = email
    set_page('upload')
    
def logout_user():
    """Log out current user"""
    st.session_state.user = None
    set_page('login')
    
def set_resume(resume_data):
    """Store processed resume data"""
    st.session_state.processed_resume = resume_data
    st.session_state.original_resume = resume_data.copy()
    
def reset_resume():
    """Reset resume to original state"""
    if st.session_state.original_resume:
        st.session_state.processed_resume = st.session_state.original_resume.copy()
    
def clear_resume():
    """Clear resume data"""
    st.session_state.processed_resume = None
    st.session_state.original_resume = None