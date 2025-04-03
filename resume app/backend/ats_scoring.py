from openai import OpenAI
import config
import json
import re

# def get_gemini_ats_score(resume_text):
#     """Fetches ATS score using Google Gemini AI"""
#     prompt = f"""
#     Act as an advanced ATS (Applicant Tracking System).
#     Evaluate the resume and **ONLY return the ATS Score** in this format:

#     ATS Score: XX%

#     Do NOT include any explanations or additional text.
    
#     Resume:
#     {resume_text}
#     """

#     try:
#         model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Correct model name
#         response = model.generate_content(prompt)

#         # Extract ATS score using regex
#         score_match = re.search(r'ATS Score:\s*(\d+%)', response.text)

#         return score_match.group(0) if score_match else "ATS Score: Not Available"
    
#     except Exception as e:
#         return f"Error: {str(e)}"

def analyze_with_gpt(resume_text, job_description):
    """Use GPT to analyze resume against job description."""
    try:
        prompt = f"""
        You are an ATS (Applicant Tracking System) expert. Analyze the resume below against the job description.
        
        JOB DESCRIPTION:
        
        {job_description.text}

        
        Required Skills: {', '.join(job_description.skills)}
        
        RESUME:
        {resume_text}
        
        Please provide the following in JSON format:
        1. A match score from 0 to 100
        2. A list of matched skills from the required skills list
        3. A list of missing skills from the required skills list
        4. A short list of recommendations to improve the resume for this specific job
        
        Return ONLY valid JSON in this exact format:
        {{
          "score": 85,
          "matched_skills": ["skill1", "skill2"],
          "missing_skills": ["skill3", "skill4"],
          "recommendations": ["recommendation1", "recommendation2"]
        }}
        """
        
        client = OpenAI(
            api_key=config.CHATGPT_API_KEY

        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an ATS scoring expert. Provide accurate analysis in the exact JSON format requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        result = response.choices[0].message.content.strip()
        # Extract JSON if it's wrapped in backticks or has extra text
        match = re.search(r'{.*}', result, re.DOTALL)
        if match:
            result = match.group(0)
            
        return json.loads(result)
        
    except Exception as e:
        print(f"Error in GPT analysis: {str(e)}")
        # Return default values if GPT analysis fails
        return {
            "score": 50,
            "matched_skills": ['skills'],
            "missing_skills": job_description.skills,
            "recommendations": ["Unable to analyze resume. Please try again."]
        }