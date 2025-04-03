# frontend/api_service.py
import requests
import json
import base64
import streamlit as st
from config import BACKEND_URL
# from pdf_generator import generate_resume_pdf
from pdf_formatter.pdf_generator import generate_resume_pdf

def process_resume(file_content):
    """Send resume file to backend for processing"""
    try:
        files = {"file": ("resume.pdf", file_content, "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/process-resume/", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def save_resume(resume_data):
    """Save resume data to backend"""
    try:
        # Make a copy to avoid modifying the original
        data_to_save = {k: v for k, v in resume_data.items() if k != 'id'}
        
        response = requests.post(f"{BACKEND_URL}/save-resume", json=data_to_save)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error saving: {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def update_resume(resume_id, resume_data, overwrite=False):
    """Update an existing resume"""
    try:
        # Make a copy to avoid modifying the original
        data_to_update = {k: v for k, v in resume_data.items() if k != 'id'}
        
        response = requests.put(
            f"{BACKEND_URL}/replace-resume/{resume_id}?overwrite={str(overwrite).lower()}", 
            json=data_to_update
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error updating: {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def get_all_resumes():
    """Get all saved resumes"""
    try:
        response = requests.get(f"{BACKEND_URL}/get-resumes")
        
        if response.status_code == 200:
            return response.json() or []
        else:
            return {"error": f"Error fetching resumes: {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def get_resume_by_id(resume_id):
    """Get a specific resume by ID"""
    try:
        response = requests.get(f"{BACKEND_URL}/get-resume/{resume_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error fetching resume: {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def delete_resume(resume_id):
    """Delete a resume"""
    try:
        response = requests.delete(f"{BACKEND_URL}/delete-resume/{resume_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error deleting resume: {response.text}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def get_resume_pdf(resume_id):
    """Get PDF version of a resume"""
    try:
        response = requests.get(f"{BACKEND_URL}/get-resume/{resume_id}")
        
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        return None

# def get_resume_download_link(resume_data, filename="resume.json"):
#     """Generate a download link for resume JSON data"""
#     json_str = json.dumps(resume_data, indent=2)
#     b64 = base64.b64encode(json_str.encode()).decode()
#     href = f'<a href="data:application/json;base64,{b64}" download="{filename}" class="download-button">⬇️ Download</a>'
#     return href

def get_pdf_download_link(pdf_content, filename="resume.pdf"):
    """Generate a download link for PDF content"""
    pdf_content = generate_resume_pdf(pdf_content)
    if pdf_content is None:
        print("DEBUG: pdf_content is None. Check why generate_resume_pdf() is failing.")
        return None  # Prevent further errors
    b64 = base64.b64encode(pdf_content).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-button">⬇️ Download PDF</a>'
    return href