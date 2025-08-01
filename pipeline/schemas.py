from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from pathlib import Path


# ------------------ JOB DESCRIPTION SCHEMA ------------------

class JobDescription(BaseModel):
    """
    Schema to represent structured information extracted from a Job Description.
    """

    job_title: str = Field(..., description="The title or designation of the job")
    required_skills: List[str] = Field(..., description="List of required hard skills (e.g., Python, SQL)")
    soft_skills: Optional[List[str]] = Field(default=[], description="List of soft skills (e.g., communication)")
    years_of_experience: Optional[int] = Field(default=None, description="Minimum years of experience required")
    degree: Optional[str] = Field(default=None, description="Educational degree required (e.g., Bachelor's, Master's)")
    tools_and_platforms: Optional[List[str]] = Field(default=[], description="Tools or platforms mentioned (e.g., AWS, Tableau)")
    certifications: Optional[List[str]] = Field(default=[], description="Certifications required or preferred (e.g., AWS Certified)")

# ------------------ RESUME SCHEMA ------------------

class ContactInfo(BaseModel):
    """
    Schema for contact information within a Resume.
    """
    phone: Optional[str] = Field(default=None, description="Candidate's phone number")
    email: Optional[EmailStr] = Field(default=None, description="Candidate's email address")
    address: Optional[str] = Field(default=None, description="Candidate's address (city, state, country)")

class ResumeSchema(BaseModel):
    """
    Schema to represent structured information extracted from a Resume.
    """

    full_name: str = Field(..., description="Candidate's full name")
    contact_info: ContactInfo = Field(..., description="Dictionary with phone, email, and optionally address") # Changed type to ContactInfo
    education: List[str] = Field(..., description="List of education entries (degrees, institutions)")
    technical_skills: List[str] = Field(..., description="List of technical or programming skills")
    experience: List[str] = Field(..., description="List of previous work experience details")
    projects: Optional[List[str]] = Field(default=[], description="List of notable projects from the resume")
    certifications: Optional[List[str]] = Field(default=[], description="List of certifications mentioned in the resume")
    summary: Optional[str] = Field(default=None, description="Candidate's personal summary or objective statement")

# ------------------ PATH SCHEMA ------------------

class FileInput(BaseModel):
    """
    schema for file input, typically used for file uploads."""
    file_path: Path = Field(..., description="The path to the file to be uploaded")

