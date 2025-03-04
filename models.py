from sqlalchemy import Column, Integer, String
from database import Base

class JobListing(Base):
    __tablename__ = "job_listings" # Table name in the database
    
    id = Column(Integer, primary_key=True, index=True) # Unique job ID (Primary Key)
    title = Column(String, index=True) # Job title (e.g. "Software Engineer")
    company = Column(String, index=True) # Company name (e.g. "MathWorks")
    location = Column(String, index=True) # Job location (e.g. "Natick")
    salary = Column(Integer) # Salary for the job (e.g., 120000)