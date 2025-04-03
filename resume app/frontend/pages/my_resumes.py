import streamlit as st
import requests
import uuid
import json
from components.header import show_header
from api_service import get_pdf_download_link
from config import BACKEND_URL

def render_page():
    if not st.session_state.user:
        st.warning("Please login to access this page.")
        st.session_state.page = 'login'
        st.rerun()

    show_header(show_logout=True)
    st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>MY RESUMES</h1>", unsafe_allow_html=True)
    
    if st.button("➕ Add New Resume", use_container_width=False):
        st.session_state.page = 'upload'
        st.rerun()
    
    try:
        # Fetch all resumes from the backend
        response = requests.get(f"{BACKEND_URL}/get-resumes")
        
        if response.status_code == 200:
            saved_resumes = response.json() or []
                
            if not saved_resumes:
                st.info("You haven't saved any resumes yet. Process a resume and save it to see it here.")
            else:
                for index, resume in enumerate(saved_resumes, start=1):
                    if not isinstance(resume, dict):
                        continue
                    
                    resume_id = resume.get('id', str(uuid.uuid4()))
                    name = resume.get('name', 'Unnamed')
                    email = resume.get('contact_info', {}).get('email', 'N/A')
                    phone = resume.get('contact_info', {}).get('phone', 'N/A')

                    # Extract skills as a flat list
                    skills_list = []
                    for domain, skills in resume.get('skills', {}).items():
                        if isinstance(skills, list):
                            skills_list.extend(skills)
                        elif isinstance(skills, str):
                            skills_list.append(skills)

                    skills_text = ', '.join(skills_list) if skills_list else 'N/A'
                            
                    st.markdown(f"""
                        <div class='resume-card'>
                            <h3 style='color: #8B7FD3;'>Resume #{index}: {name}</h3>
                            <p><strong>Email:</strong> {email}</p>
                            <p><strong>Phone:</strong> {phone}</p>
                            <p><strong>Skills:</strong> {skills_text}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("👁️ View", key=f"view_{resume_id}"):
                            try:
                                detail_response = requests.get(f"{BACKEND_URL}/get-resume/{resume_id}")
                                if detail_response.status_code == 200:
                                    detailed_resume = detail_response.json()
                                    if detailed_resume:
                                        st.session_state.processed_resume = detailed_resume
                                        st.session_state.original_resume = detailed_resume.copy()
                                        st.session_state.page = 'preview'
                                        st.rerun()
                                    else:
                                        st.error("Could not retrieve resume details")
                                else:
                                    st.error(f"Error fetching resume details: {detail_response.text}")
                            except Exception as e:
                                st.error(f"Error connecting to backend: {str(e)}")
                                st.session_state.processed_resume = resume
                                st.session_state.original_resume = resume.copy()
                                st.session_state.page = 'preview'
                                st.rerun()

                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{resume_id}"):
                            try:
                                detail_response = requests.get(f"{BACKEND_URL}/get-resume/{resume_id}")
                                if detail_response.status_code == 200:
                                    detailed_resume = detail_response.json()
                                    if detailed_resume:
                                        st.session_state.processed_resume = detailed_resume
                                        st.session_state.original_resume = detailed_resume.copy()
                                        st.session_state.page = 'edit'
                                        st.rerun()
                                    else:
                                        st.error("Could not retrieve resume details")
                                else:
                                    st.error(f"Error fetching resume details: {detail_response.text}")
                            except Exception as e:
                                st.error(f"Error connecting to backend: {str(e)}")
                                st.session_state.processed_resume = resume
                                st.session_state.original_resume = resume.copy()
                                st.session_state.page = 'edit'
                                st.rerun()

                    with col3:
                        try:
                            response_resume_pdf = requests.get(f"{BACKEND_URL}/get-resume/{resume_id}")
                            if response_resume_pdf.status_code == 200:
                                resume_data = response_resume_pdf.json()
                                href = get_pdf_download_link(resume_data)
                                st.markdown(href, unsafe_allow_html=True)
                            else:
                                st.error("Failed to fetch PDF. Please try again.")
                        except Exception as e:
                            st.error(f"Error preparing download: {str(e)}")

                    with col4:
                        if st.button("🗑️ Delete", key=f"delete_{resume_id}"):
                            try:
                                delete_response = requests.delete(f"{BACKEND_URL}/delete-resume/{resume_id}")
                                if delete_response.status_code == 200:
                                    st.success(f"Resume #{index} deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Error deleting resume: {delete_response.text}")
                            except Exception as e:
                                st.error(f"Error connecting to backend: {str(e)}")
        else:
            st.error(f"Error fetching resumes: {response.text}")
    except Exception as e:
        st.error(f"Error loading saved resumes: {str(e)}")
