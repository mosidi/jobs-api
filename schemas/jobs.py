from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    job_title: Optional[str] = None
    job_company: Optional[str] = None
    job_company_url: Optional[str] = None
    job_location: Optional[str] = "Remote"
    job_description: Optional[str] = None
    job_date_posted: Optional[date] = datetime.now().date()


class JobCreate(JobBase):
    job_title: str
    job_company: str
    job_location: str
    job_description: str


class ShowJob(JobBase):
    job_title: str
    job_company: str
    job_company_url: Optional[str]
    job_location: str
    job_date_posted: date
    job_description: Optional[str]

    class Config:
        orm_mode = True
