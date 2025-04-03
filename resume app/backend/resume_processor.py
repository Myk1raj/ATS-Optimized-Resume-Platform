import requests
from PyPDF2 import PdfReader
from io import BytesIO
import json
import config

def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file"""
    try:
        reader = PdfReader(pdf_file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text.strip() if text else ""
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def analyze_resume_with_gemini(resume_text):
    """Process resume text using Gemini API"""
    prompt = f'''
    This is a resume:
    {resume_text}

    Please analyze the resume and format it into the following structured JSON format:
    For their skills, logically classify all the skills mention into groups of domains, and add represent them in a list form. The domains for example but not limited to Frontend, Backend, Ai/ml, devops, testing, reserach, etc
    ** important : The output you give must never contain "&"
    {{
        "name": "",
        "summary": "a 5-6 word title",
        "about": "summary of the entire resume",
        "contact_info": {{
            "address": "",
            "phone": "",
            "email": ""
        }},
        "personal_info": {{
            "dob": "DD/MM/YYYY",
            "nationality": ""
        }},
        "platforms": {{
            "github": "",
            "linkedin": ""
        }},
        "languages": [
            {{"name": "", "fluency": "", "country": ""}}
        ],
        "education": [
            {{
                "period": "Year-Year",
                "university": "",
                "details": ["Course", "GPA", "Remarks"]
            }}
        ],
        "work_experience": [
            {{
                "period": "Year-Year",
                "company": "",
                "roles": ["Position", "Projects"]
            }}
        ],
        "publications": [
            {{"year": "", "topic": ""}}
        ],
        "awards": [
            {{"year": "", "prize": ""}}
        ],
        "memberships": [
            {{"year": "", "organization": "", "position": ""}}
        ],
        "skills": {{
            "Domain1": [],
            "Domain2": [],
        }},
        "image": "images/image.tex"
    }}
    '''

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }
    
    try:
        response = requests.post(config.GEMINI_URL, headers=headers, json=data)
        response_json = response.json()
        
        if response.status_code == 200 and "candidates" in response_json:
            response_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(response_text)  # Ensure it's a valid JSON format
        else:
            return {"error": f"Failed to get data from Gemini API. Status: {response.status_code}, Response: {response_json}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format returned by Gemini API"}
    except Exception as e:
        return {"error": f"Error processing resume: {str(e)}"}

def process_resume_file(file_content):
    """Process resume file and return structured data"""
    try:
        pdf_file = BytesIO(file_content)
        resume_text = extract_text_from_pdf(pdf_file)
        
        if not resume_text:
            return {"error": "No text could be extracted from the PDF."}
        
        result = analyze_resume_with_gemini(resume_text)
        return result
    except Exception as e:
        return {"error": f"Error processing resume: {str(e)}"}