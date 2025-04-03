from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Optional

class ContactInfo(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class PersonalInfo(BaseModel):
    dob: Optional[str] = None
    nationality: Optional[str] = None

class Education(BaseModel):
    period: Optional[str] = None  # "Year-Year"
    university: Optional[str] = None
    details: List[str] = []  # ["Course", "Gpa", "Remarks"]

class Experience(BaseModel):
    period: Optional[str] = None  # "Year-Year"
    company: Optional[str] = None
    roles: List[str] = []

class Publication(BaseModel):
    year: Optional[str] = None
    topic: Optional[str] = None

class Award(BaseModel):
    year: Optional[str] = None
    prize: Optional[str] = None

class Membership(BaseModel):
    year: Optional[str] = None
    organization: Optional[str] = None
    position: Optional[str] = None

class Resume(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None  # A 5-6 word title
    about: Optional[str] = None  # Summary of the entire resume
    contact_info: ContactInfo = ContactInfo()
    personal_info: PersonalInfo = PersonalInfo()
    platforms: Dict[str, Optional[str]] = {"github": "", "linkedin": ""}  # {"github": "", "linkedin": "", "others": ""}
    languages: List[Tuple[str, str, str]] = []
    education: List[Education] = []
    work_experience: List[Experience] = []
    publications: List[Publication] = []
    awards: List[Award] = []
    memberships: List[Membership] = []
    skills: Dict[str, List[str]] = {}  # {"Domain1": [...], "Domain2": [...]}
    image: Optional[str] = "images/image.tex"

class JobDescription(BaseModel):
    text: str
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None

class AnalyzeRequest(BaseModel):
    resumes: List[str] = []
    job_description: JobDescription
