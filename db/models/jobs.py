from db.base_class import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Job(Base):
    """
    A Job represents a job posting, with details such as job title, company, location,
    description, and the id of the user who owns the job.
    """

    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    job_company = Column(String, nullable=False)
    job_company_url = Column(String)
    job_location = Column(String, nullable=False)
    job_description = Column(String, nullable=False)
    job_date_posted = Column(Date)
    job_is_active = Column(Boolean(), default=True)
    job_owner_id = Column(Integer, ForeignKey("user.id"))
    job_owner = relationship("User", back_populates="jobs")
