# backend/routes/resume_routes.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List

import database
import resume_processor
from models import Resume,JobDescription,AnalyzeRequest
from ats_scoring import analyze_with_gpt

router = APIRouter()

@router.post("/process-resume/")
async def process_resume(file: UploadFile = File(...)):
    """Process a resume file and extract structured data"""
    try:
        # Read the uploaded file
        file_content = await file.read()
        
        # Process the resume file
        result = resume_processor.process_resume_file(file_content)
        
        if "error" in result:
            return JSONResponse(
                status_code=400, 
                content={"error": result["error"]}
            )
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-resume")
async def save_resume(resume: Resume):
    """Save a new resume to the database"""
    result = database.save_resume(resume)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to save resume")
        
    return result

@router.get("/get-resumes")
async def get_resumes():
    """Get all resumes from the database"""
    try:
        resumes = database.get_all_resumes()
        return resumes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-resume/{id}")
async def get_resume(id: str):
    """Get a specific resume by ID"""
    resume = database.get_resume_by_id(id)
    
    if not resume:
        return JSONResponse(content={"message": "Resume not found"})
        
    return resume

@router.delete("/delete-resume/{id}")
async def delete_resume(id: str):
    """Delete a resume from the database"""
    success = database.delete_resume(id)
    
    if success:
        return {"message": "Resume deleted successfully"}
    else:
        return {"message": "Resume not found"}

@router.put("/replace-resume/{id}")
async def replace_resume(id: str, resume: Resume, overwrite: bool = Query(False)):
    """Update an existing resume or handle duplicates"""
    result = database.update_resume(id, resume, overwrite)
    return result

@router.get("/get-resumes-by-skill/{skill}")
async def get_resumes_by_skill(skill: str):
    """Get all resumes with a specific skill"""
    try:
        resumes = database.get_resumes_by_skill(skill)
        return resumes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/analyze-resumes/")
async def analyze_resume(job_description:JobDescription):
    resumes = database.get_all_resumes()
    results = []
    try:
        for resume in resumes:
            resume_id = resume.get("id", "Unknown")
            resume_text = resume.get("text", "")
            analysis = analyze_with_gpt(resume, job_description)
            
            results.append ({
                "resume":resume_id,
                "score":analysis["score"],
                # matched_skills=analysis["matched_skills"],
                # missing_skills=analysis["missing_skills"],
                # recommendations=analysis["recommendations"]
            })
        
        return jsonable_encoder({"results": sorted(results, key=lambda x: x["score"], reverse=True)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")