import streamlit as st

def show_header(show_logout=False):
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col1:
        st.image("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-zp9zWsbz7ZgvW9RTld0KF2sQMB5Riw.png", width=200)
    with col3:
        if st.button("🏠 Home"):
            st.session_state.page = 'upload'
            st.rerun()
    if st.session_state.user and (show_logout or st.session_state.page == 'my_resumes'):
        with col4:
            if st.button("🔒 Logout", key="logout_button"):
                st.session_state.user = None
                st.session_state.page = 'login'
                st.rerun()