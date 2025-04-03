# backend/database.py
from pymongo import MongoClient
import config
import uuid
from models import Resume

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
resumes_collection = db[config.COLLECTION_NAME]

def save_resume(resume: Resume):
    """Save resume to database with a generated ID"""
    resume_id = str(uuid.uuid4())
    resume_dict = resume.dict()
    resume_dict["id"] = resume_id
    
    result = resumes_collection.insert_one(resume_dict)
    return {"resume_id": resume_id} if result.inserted_id else None

def update_resume(resume_id: str, resume: Resume, overwrite: bool = False):
    """Update an existing resume by ID"""
    # Check if the resume exists
    existing_resume = resumes_collection.find_one({"id": resume_id})
    if not existing_resume:
        return {"message": "Resume not found"}

    # # Extract email from incoming resume data
    # new_email = resume.contact_info.get("email","").lower()
    
    # # Check for duplicates with the same email but different ID
    # if new_email:
    #     duplicate_resume = resumes_collection.find_one({
    #         "contact_info.email": new_email,
    #         "id": {"$ne": resume_id}
    #     })
        
    #     if duplicate_resume and not overwrite:
    #         return {"message": "A duplicate resume exists with this email"}
            
    #     if duplicate_resume and overwrite:
    #         resumes_collection.delete_one({"id": duplicate_resume["id"]})
    
    # Update the resume
    resume_dict = resume.dict()
    resume_dict["id"] = resume_id
    
    result = resumes_collection.replace_one({"id": resume_id}, resume_dict)
    return {"resume_id": resume_id, "message": "Resume updated successfully"} if result.modified_count else {"message": "No changes made"}

def get_all_resumes():
    """Get all resumes from the database"""
    return list(resumes_collection.find({}, {"_id": 0}))

def get_resume_by_id(resume_id: str):
    """Get a resume by its ID"""
    return resumes_collection.find_one({"id": resume_id}, {"_id": 0})

def delete_resume(resume_id: str):
    """Delete a resume by its ID"""
    result = resumes_collection.delete_one({"id": resume_id})
    return result.deleted_count == 1

def get_resumes_by_skill(skill: str):
    """Get resumes that have a specific skill"""
    query = {
        "skills": {
            "$elemMatch": {
                "$regex": skill,
                "$options": "i"
            }
        }
    }
    return list(resumes_collection.find(query, {"_id": 0}))