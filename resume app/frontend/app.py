# frontend/app.py
import streamlit as st
from ui import styles
from pages import login, upload, preview, edit, my_resumes, search
import session

def main():
    # Apply custom styles
    styles.apply_styles()
    
    # Initialize session state if needed
    session.initialize_session()
    
    # Display current page based on session state
    if st.session_state.page == 'login':
        login.render_page()
    elif st.session_state.page == 'upload':
        upload.render_page()
    elif st.session_state.page == 'preview':
        preview.render_page()
    elif st.session_state.page == 'edit':
        edit.render_page()
    elif st.session_state.page == 'my_resumes':
        my_resumes.render_page()
    elif st.session_state.page == 'search':
        search.render_page()
    else:
        login.render_page()

if __name__ == "__main__":
    main()