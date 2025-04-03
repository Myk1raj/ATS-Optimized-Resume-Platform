import streamlit as st
import requests
import json
from components.header import show_header
from api_service import get_pdf_download_link
from config import BACKEND_URL

def clean_json(data):
    """ Recursively clean None values in the dictionary """
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [clean_json(v) for v in data if v is not None]
    return data

def render_page():
    if not st.session_state.user:
        st.warning("Please login to access this page.")
        st.session_state.page = 'login'
        st.rerun()

    show_header()
    st.markdown("""
        <h1 style='text-align: center; background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>RESUME PREVIEW</h1>
    """, unsafe_allow_html=True)
    
    if st.session_state.processed_resume:
        resume = st.session_state.processed_resume
        
        with st.container():
            # Name and Summary
            st.markdown(f"## {resume.get('name', 'Name not provided')}")
            st.markdown(f"### {resume.get('summary', '')}")
            
            # About Section
            if resume.get('about'):
                st.markdown("### About")
                st.write(resume.get('about', ''))
            
            # Contact Information
            st.markdown("### Contact Information")
            contact_info = resume.get('contact_info', {})
            platforms = resume.get('platforms', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if contact_info.get('email'):
                    st.text_input("Email", value=contact_info.get('email', ''), disabled=True)
            with col2:
                if contact_info.get('phone'):
                    st.text_input("Phone", value=contact_info.get('phone', ''), disabled=True)
            with col3:
                if contact_info.get('address'):
                    st.text_input("Address", value=contact_info.get('address', ''), disabled=True)
            
            # Platforms
            if any(platforms.values()):
                st.markdown("### Online Platforms")
                platform_cols = st.columns(2)
                with platform_cols[0]:
                    if platforms.get('github'):
                        st.text_input("GitHub", value=platforms.get('github', ''), disabled=True)
                with platform_cols[1]:
                    if platforms.get('linkedin'):
                        st.text_input("LinkedIn", value=platforms.get('linkedin', ''), disabled=True)
            
            # Skills
            st.markdown("### Skills")
            skills = resume.get('skills', {})
            
            # Create a more dynamic grid based on number of skill categories
            num_categories = len(skills)
            if num_categories > 0:
                # Calculate number of columns (max 3)
                num_cols = min(3, num_categories)
                skills_cols = st.columns(num_cols)
                
                for idx, (category, skills_list) in enumerate(skills.items()):
                    if skills_list:  # Only show categories with skills
                        with skills_cols[idx % num_cols]:
                            # Filter out None values
                            filtered_skills = [skill for skill in skills_list if skill is not None]
                            if filtered_skills:
                                formatted_skills = ", ".join(filtered_skills)
                                st.text_area(category, value=formatted_skills, disabled=True, height=100)
            
            # Education
            st.markdown("### Education")
            education_list = resume.get('education', [])
            for i, edu in enumerate(education_list):
                with st.expander(f"{edu.get('university', 'Unknown University')} - {edu.get('period', '')}"):
                    # Filter out None values and ensure all items are strings
                    filtered_details = []
                    for detail in edu.get('details', []):
                        if detail is not None:
                            if isinstance(detail, str):
                                filtered_details.append(detail)
                            elif isinstance(detail, (list, tuple)):
                                # Convert nested lists to strings
                                filtered_details.append(", ".join(str(item) for item in detail if item is not None))
                            else:
                                filtered_details.append(str(detail))
                    
                    if filtered_details:
                        st.markdown("- " + "\n- ".join(filtered_details))
            
            # Work Experience
            st.markdown("### Work Experience")
            experience_list = resume.get('work_experience', [])
            for i, exp in enumerate(experience_list):
                with st.expander(f"{exp.get('company', 'Unknown Company')} - {exp.get('period', '')}"):
                    # Filter out None values and ensure all items are strings
                    filtered_roles = []
                    for role in exp.get('roles', []):
                        if role is not None:
                            if isinstance(role, str):
                                filtered_roles.append(role)
                            elif isinstance(role, (list, tuple)):
                                # Convert nested lists to strings
                                filtered_roles.append(", ".join(str(item) for item in role if item is not None))
                            else:
                                filtered_roles.append(str(role))
                    
                    if filtered_roles:
                        st.markdown("- " + "\n- ".join(filtered_roles))
            
            # Awards
            if resume.get('awards'):
                st.markdown("### Awards & Achievements")
                for award in resume.get('awards', []):
                    st.markdown(f"- **{award.get('year', '')}**: {award.get('prize', '')}")
            
            # Languages
            languages = resume.get('languages', [])
            if languages:
                st.markdown("### Languages")
                # Handle different possible formats for languages
                if isinstance(languages, list):
                    language_items = []
                    for lang in languages:
                        if isinstance(lang, str):
                            language_items.append(lang)
                        elif isinstance(lang, dict):
                            # If it's a dict, try to extract the language name and proficiency
                            lang_name = lang.get('name', '') or lang.get('language', '')
                            proficiency = lang.get('proficiency', '') or lang.get('level', '')
                            if lang_name and proficiency:
                                language_items.append(f"{lang_name} ({proficiency})")
                            elif lang_name:
                                language_items.append(lang_name)
                        else:
                            # Convert any other type to string
                            language_items.append(str(lang))
                    
                    if language_items:
                        st.write(", ".join(language_items))
                elif isinstance(languages, dict):
                    # If languages is a dict, display each language and its proficiency
                    for lang, proficiency in languages.items():
                        st.write(f"- {lang}: {proficiency}")
                else:
                    # If it's some other format, just convert to string
                    st.write(str(languages))
            
            # Action Buttons
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✏️ Edit Resume", use_container_width=True):
                    st.session_state.page = 'edit'
                    st.rerun()
            
            with col2:
                if st.button("💾 Save Resume", use_container_width=True):
                    try:
                        # Fix languages field
                        if isinstance(resume.get("languages"), list):
                            resume["languages"] = [
                                (lang.get("name", ""), lang.get("proficiency", ""), lang.get("country", ""))
                                if isinstance(lang, dict) else lang
                                for lang in resume["languages"]
                            ]

                        # Fix work_experience roles
                        if "work_experience" in resume:
                            for exp in resume["work_experience"]:
                                if isinstance(exp.get("roles"), list):
                                    exp["roles"] = [item if isinstance(item, str) else ", ".join(item) for item in exp["roles"]]

                        # Clean JSON and send request
                        resume_data = clean_json(resume)
                        response = requests.post(f"{BACKEND_URL}/save-resume", json=resume_data)
                        
                        if response.status_code == 200:
                            st.success("Resume saved successfully!")
                            st.session_state.page = 'my_resumes'
                            st.rerun()
                        else:
                            st.error(f"Error saving: {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")

            
            with col3:
                href = get_pdf_download_link(resume)
                st.markdown(href, unsafe_allow_html=True)
            
            with col4:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.processed_resume = None
                    st.session_state.page = 'upload'
                    st.rerun()