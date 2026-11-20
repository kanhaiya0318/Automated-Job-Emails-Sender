from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional



class JobListing(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = Field(default=None, description="job role as it is if mentioned in post")
    is_role_relevant: bool = Field(description="True only for full time or Internship in AI/ML/GenAI/LLM or Python backend roles. False for data analyst, data governance, sales, ERP/HCM, testing etc.")
    location: Optional[str] = None
    location_in_india_or_unspecified: bool = Field(description="True if the job is in India, remote, or has no location mentioned; False only if it is based in or restricted to a country outside India.")
    min_experience_years: Optional[float] = Field(None, description="Lowest experience required for THIS job; None if not stated")
    contact_email: Optional[str] = Field(None, description="Email for THIS job. Copy from the candidate emails; None if none belongs to this job")
    apply_link: Optional[str] = Field(None, description="Application/job-page/form URL for THIS job. Not hashtags, bootcamps, courses or promo links")
    whatsapp_or_phone: Optional[str] = Field(None, description="WhatsApp or phone number for THIS job, exactly as written")
    is_dm_on_linkedin:bool = Field(description="True is post say to dm on linkedin otherwise False")
    application_requirements: Optional[str] = Field(None, description="What applicants requirements and skills requirements, e.g. Immediate joiner, python, langgraph, AI/ML, Enterprise Agentic AI, Generative AI solutions..etc.")

class PostExtraction(BaseModel):
    is_hiring_post: bool = Field(description="True for Employer/recruiter hiring. False for job seekers, ads, general posts")
    jobs: list[JobListing] = Field(default_factory=list, description="One entry per distinct job in the post")

class relevant_job(JobListing):
    is_positive_email:bool = False
    is_whatsapp_contact:bool = False
    is_link:bool = False
    apply_methods:Optional[list[str]] = None
    reason:Optional[str] = None