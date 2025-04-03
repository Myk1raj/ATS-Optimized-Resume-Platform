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
    st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #8B7FD3 0%, #9B8FE3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>EDIT RESUME</h1>", unsafe_allow_html=True)
    
    if st.session_state.processed_resume:
        resume = st.session_state.processed_resume
        
        with st.form("edit_resume_form"):
            st.markdown("<div class='form-like'>", unsafe_allow_html=True)
            
            # Personal Information Section
            st.markdown("<div class='section-header'>Personal Information</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                resume['name'] = st.text_input("Name", value=resume.get('name', ''))
                resume['contact_info']['email'] = st.text_input("Email", value=resume['contact_info'].get('email', ''))
            with col2:
                resume['contact_info']['phone'] = st.text_input("Phone", value=resume['contact_info'].get('phone', ''))
                resume['contact_info']['address'] = st.text_input("Address", value=resume['contact_info'].get('address', ''))

            # Personal Details
            st.markdown("<div class='section-header'>Personal Details</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                resume['personal_info']['dob'] = st.text_input("Date of Birth (DD/MM/YYYY)", value=resume['personal_info'].get('dob', 'DD/MM/YYYY'))
            with col2:
                resume['personal_info']['nationality'] = st.text_input("Nationality", value=resume['personal_info'].get('nationality', ''))
            
            # Platforms
            st.markdown("<div class='section-header'>Platforms</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if 'platforms' not in resume:
                    resume['platforms'] = {}
                resume['platforms']['github'] = st.text_input("GitHub", value=resume.get('platforms', {}).get('github', ''))
            with col2:
                resume['platforms']['linkedin'] = st.text_input("LinkedIn", value=resume.get('platforms', {}).get('linkedin', ''))

            # Skills Section
            st.markdown("<div class='section-header'>Skills</div>", unsafe_allow_html=True)
            skills_cols = st.columns(3)
            for idx, (category, skills) in enumerate(resume['skills'].items()):
                with skills_cols[idx % 3]:
                    updated_skills = st.text_input(category, value=", ".join(skills) if skills else "")
                    resume['skills'][category] = [skill.strip() for skill in updated_skills.split(",")] if updated_skills else []

            # Work Experience Section
            st.markdown("<div class='section-header'>Work Experience</div>", unsafe_allow_html=True)
            for i, exp in enumerate(resume['work_experience']):
                with st.expander(f"Experience {i+1} - {exp.get('company', '')}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if isinstance(exp, dict):
                            exp['company'] = st.text_input("Company", value=exp.get('company', ''), key=f"edit_company_{i}")
                        else:
                            # Handle list format from the JSON
                            company = exp[1] if len(exp) > 1 and exp[1] is not None else ''
                            company_input = st.text_input("Company", value=company, key=f"edit_company_{i}")
                            if len(exp) > 1:
                                exp[1] = company_input
                    with col2:
                        if isinstance(exp, dict):
                            exp['period'] = st.text_input("Duration", value=exp.get('period', ''), key=f"edit_duration_{i}")
                        else:
                            # Handle list format from the JSON
                            period = exp[0] if len(exp) > 0 and exp[0] is not None else ''
                            period_input = st.text_input("Duration", value=period, key=f"edit_duration_{i}")
                            if len(exp) > 0:
                                exp[0] = period_input
                    
                    if isinstance(exp, dict):
                        roles = exp.get('roles', [])
                        if roles is None:
                            roles = []
                        roles = [str(detail) for detail in roles if detail is not None]
                        print("pokemon")
                        print(roles)
                        roles_str = "\n".join(roles)
                        
                        updated_roles = st.text_area("Positions & Projects (one per line)", value=roles_str, key=f"edit_roles_{i}")
                        exp['roles'] = [role.strip() for role in updated_roles.split("\n") if role.strip()]
                    else:
                        # Handle list format from the JSON
                        roles = exp[2] if len(exp) > 2 and exp[2] is not None else []
                        if not isinstance(roles, list):
                            roles = [roles] if roles else []
                        roles_str = "\n".join([r for r in roles if r is not None])
                        updated_roles = st.text_area("Positions & Projects (one per line)", value=roles_str, key=f"edit_roles_{i}")
                        if len(exp) > 2:
                            exp[2] = [role.strip() for role in updated_roles.split("\n") if role.strip()]

            # Education Section
            st.markdown("<div class='section-header'>Education</div>", unsafe_allow_html=True)
            for i, edu in enumerate(resume['education']):
                with st.expander(f"Education {i+1} - {edu.get('university', '')}", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        if isinstance(edu, dict):
                            edu['university'] = st.text_input("University", value=edu.get('university', ''), key=f"edit_university_{i}")
                        else:
                            # Handle list format from the JSON
                            university = edu[1] if len(edu) > 1 and edu[1] is not None else ''
                            university_input = st.text_input("University", value=university, key=f"edit_university_{i}")
                            if len(edu) > 1:
                                edu[1] = university_input
                    with col2:
                        if isinstance(edu, dict):
                            edu['period'] = st.text_input("Period", value=edu.get('period', ''), key=f"edit_period_{i}")
                        else:
                            # Handle list format from the JSON
                            period = edu[0] if len(edu) > 0 and edu[0] is not None else ''
                            period_input = st.text_input("Period", value=period, key=f"edit_period_{i}")
                            if len(edu) > 0:
                                edu[0] = period_input
                    
                    if isinstance(edu, dict):
                        details = edu.get('details', [])
                        if details is None:
                            details = []
                        details = [detail for detail in details if detail is not None]
                        details_str = "\n".join(details)
                        updated_details = st.text_area("Details (one per line)", value=details_str, key=f"edit_details_{i}")
                        edu['details'] = [detail.strip() for detail in updated_details.split("\n") if detail.strip()]
                    else:
                        # Handle list format from the JSON
                        details = edu[2] if len(edu) > 2 and edu[2] is not None else []
                        if not isinstance(details, list):
                            details = [details] if details else []
                        details_str = "\n".join([d for d in details if d is not None])
                        updated_details = st.text_area("Details (one per line)", value=details_str, key=f"edit_details_{i}")
                        if len(edu) > 2:
                            edu[2] = [detail.strip() for detail in updated_details.split("\n") if detail.strip()]

            # Awards Section
            if resume.get('awards'):
                st.markdown("<div class='section-header'>Awards</div>", unsafe_allow_html=True)
                for i, award in enumerate(resume['awards']):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if isinstance(award, dict):
                            award['prize'] = st.text_input("Achievement", value=award.get('prize', ''), key=f"edit_award_{i}")
                        else:
                            # This is unlikely but included for completeness
                            st.text_input("Achievement", value=award, key=f"edit_award_{i}")
                    with col2:
                        if isinstance(award, dict):
                            award['year'] = st.text_input("Year", value=award.get('year', ''), key=f"edit_year_{i}")
                        else:
                            # This is unlikely but included for completeness
                            st.text_input("Year", value="", key=f"edit_year_{i}")

            # Candidate Summary Section
            st.markdown("<div class='section-header'>Candidate Summary</div>", unsafe_allow_html=True)
            resume['about'] = st.text_area("Professional Summary", value=resume.get('about', ''), height=150)
            
            # Summary field (displayed at the top of resume)
            st.markdown("<div class='section-header'>Resume Headline</div>", unsafe_allow_html=True)
            resume['summary'] = st.text_input("Headline/Title", value=resume.get('summary', ''))

            st.markdown("</div>", unsafe_allow_html=True)
            
            # Form Controls (submit buttons)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                discard_changes = st.form_submit_button("❌ Discard Changes", use_container_width=True)
            with col2:
                save_changes = st.form_submit_button("💾 Save Changes", use_container_width=True)
            with col3:
                reset_form = st.form_submit_button("🔄 Reset", use_container_width=True)
        
        # Handle form submit actions outside the form
        if discard_changes:
            if hasattr(st.session_state, 'original_resume') and st.session_state.original_resume:
                st.session_state.processed_resume = st.session_state.original_resume.copy()
            st.session_state.page = 'preview'
            st.rerun()
            
        if save_changes:
            try:
                # Make a copy of the resume data to avoid modifying the original
                resume_data = resume.copy()
                resume_id = resume_data.pop('id', None)

                if resume_id:
                    response = requests.put(
                        f"{BACKEND_URL}/replace-resume/{resume_id}?overwrite=true",
                        json=resume_data
                    )
                else:
                    response = requests.post(f"{BACKEND_URL}/save-resume", json=resume_data)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'resume_id' in result:
                        st.session_state.processed_resume['id'] = result['resume_id']
                    elif resume_id:
                        st.session_state.processed_resume['id'] = resume_id
                        
                    st.success("Changes saved successfully!")
                    st.session_state.page = 'preview'
                    st.rerun()
                else:
                    st.error(f"Error saving changes: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
                
        if reset_form:
            if hasattr(st.session_state, 'original_resume') and st.session_state.original_resume:
                st.session_state.processed_resume = st.session_state.original_resume.copy()
                st.success("Resume reset to original version!")
                st.rerun()