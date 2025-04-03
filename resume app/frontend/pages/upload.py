import streamlit as st
import requests
from components.header import show_header
from config import BACKEND_URL

def render_page():
    if not st.session_state.user:
        st.warning("Please login to access this page.")
        st.session_state.page = 'login'
        st.rerun()

    show_header()
    st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>RESUME CRAFTER</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add New Resume", use_container_width=True):
            st.session_state.processed_resume = None
            st.rerun()
    with col2:
        if st.button("📁 My Resumes", use_container_width=True):
            st.session_state.page = 'my_resumes'
            st.rerun()
    with col3:
        if st.button("🔍 Search & Match", use_container_width=True):
            st.session_state.page = 'search'
            st.rerun()
    
    st.markdown("""
        <div class='upload-section'>
            <h3>Upload your resume (PDF format)</h3>
            <p>or drop it here</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['pdf'])
    
    if uploaded_file:
        with st.spinner("Processing resume..."):
            try:
                files = {"file": ("resume.pdf", uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{BACKEND_URL}/process-resume/", files=files)
                if response.status_code == 200:
                    processed_resume = response.json()

                    # Store the processed resume in session state
                    st.session_state.processed_resume = processed_resume
                    st.session_state.original_resume = processed_resume.copy()
                    st.success("Resume processed successfully!")
                    st.session_state.page = 'preview'
                    st.rerun()
                else:
                    st.error(f"Error processing resume: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to backend: {str(e)}")