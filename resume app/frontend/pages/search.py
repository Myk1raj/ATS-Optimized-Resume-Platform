import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from components.header import show_header
from config import BACKEND_URL
import json

from api_service import get_pdf_download_link

def render_page():
    if not st.session_state.user:
        st.warning("Please login to access this page.")
        st.session_state.page = 'login'
        st.rerun()

    # Initialize session state variables
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'skills' not in st.session_state:
        st.session_state.skills = []
    if 'education' not in st.session_state:
        st.session_state.education = ""
    if 'experience' not in st.session_state:
        st.session_state.experience = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    show_header()
    st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>RESUME MATCH</h1>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
    with col2:
        if st.button("📁 My Resumes", use_container_width=True):
            st.session_state.page = 'my_resumes'
            st.rerun()
    with col3:
        if st.button("➕ Add New Resume", use_container_width=True):
            st.session_state.processed_resume = None
            st.session_state.page = 'upload'
            st.rerun()
    
    # Two columns layout for job description and results
    job_col, results_col = st.columns([1, 2])
        
    # Job description input column
    with job_col:
        st.subheader("Job Description")
        st.session_state.job_description = st.text_area(
            "Paste job description here", 
            value=st.session_state.job_description,
            height=200
        )

        skills_input = st.text_area(
            "Required Skills (one per line)", 
            height=100,
            help="Enter one skill per line for precise matching."
        )
        if skills_input:
            st.session_state.skills = [skill.strip() for skill in skills_input.split('\n') if skill.strip()]

        st.session_state.education = st.text_input(
            "Required Education", 
            value=st.session_state.education,
            help="E.g., Bachelor's in Computer Science"
        )

        st.session_state.experience = st.text_input(
            "Required Experience", 
            value=st.session_state.experience,
            help="E.g., 3+ years in software development"
        )

        if st.button("Match with My Resumes", type="primary", disabled=not st.session_state.job_description):
            with st.spinner("Analyzing your resumes..."):
                try:
                    resumes_response = requests.get(f"{BACKEND_URL}/get-resumes")

                    if resumes_response.status_code != 200:
                        st.error("Failed to fetch your resumes.")
                        return

                    resumes = resumes_response.json()

                    if not resumes:
                        st.warning("You don't have any resumes uploaded. Please add a resume first.")
                        return

                    # Prepare job description data
                    job_data = {
                        "text": st.session_state.job_description,
                        "skills": st.session_state.skills,
                        "education": st.session_state.education,
                        "experience": st.session_state.experience,
                        "resume_ids": [resume['id'] for resume in resumes]  # Send resume IDs to backend
                    }

                    # Send to backend for analysis
                    analysis_response = requests.post(
                        f"{BACKEND_URL}/analyze-resumes/", 
                        json=job_data
                    )

                    if analysis_response.status_code == 200:
                        st.session_state.analysis_results = analysis_response.json()["results"]
                        st.success("Analysis complete!")
                    else:
                        st.error(f"Analysis failed: {analysis_response.text}")
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")

    # Results column
    with results_col:
        st.subheader("Results")

        # Display analysis results if they exist
        if st.session_state.analysis_results:
            for index, result in enumerate(st.session_state.analysis_results, start=1):
                resume_id = result["resume"]
                score = result["score"]

                # Fetch the actual resume details
                resume_response = requests.get(f"{BACKEND_URL}/get-resume/{resume_id}")
                if resume_response.status_code != 200:
                    st.error(f"Error fetching details for Resume {resume_id}")
                    continue

                resume = resume_response.json()

                # Ensure resume contains necessary details
                if not isinstance(resume, dict):
                    continue

                # Extract contact information
                name = resume.get("name", "Unnamed")
                contact_info = resume.get("contact_info", {})
                email = contact_info.get("email", "N/A")
                phone = contact_info.get("phone", "N/A")

                # Extract skills for display
                skills_list = resume.get("skills", [])

                skills_text = ", ".join(skills_list) if skills_list else "N/A"

                # Display analyzed resume
                st.markdown(f"""
                    <div class='resume-card' style='border: 1px solid #ddd; padding: 15px; border-radius: 8px; position: relative; margin-bottom: 15px;'>
                        <h3 style='color: #8B7FD3; display: flex; justify-content: space-between;'>
                            <span>Resume #{index}: {name}</span>
                            <span style="background-color: #f4f4f4; padding: 5px 10px; border-radius: 5px; font-size: 16px; font-weight: bold;">
                                {score} / 100
                            </span>
                        </h3>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Phone:</strong> {phone}</p>
                        <p><strong>Skills:</strong> {skills_text}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add View button for this resume
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
                        # Fallback to using the already retrieved resume data
                        st.session_state.processed_resume = resume
                        st.session_state.original_resume = resume.copy()
                        st.session_state.page = 'preview'
                        st.rerun()
        else:
            st.info("No analysis results yet. Run an analysis to see results here.")
