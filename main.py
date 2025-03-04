# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI is working again!"}

# # Dynamic path parameter
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id, "description": "This is a sample item, a dynamic path parameter."}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import JobListing

# Create the database tables
Base.metadata.create_all(bind=engine)

# initialize FastAPI
app = FastAPI()

# Define a root endpoint
@app.get("/")
def root():
    """
    Root API - Return a welcome message
    """
    return {"message": "Hello, welcome to the Job Listings API!"}

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new job listing (POST)
@app.post("/jobs/")
def create_job(title: str, company: str, location: str, salary: int, db: Session = Depends(get_db)):
    """
    Create a new job listing and save it to the database.

    Args:
        title (str): _description_
        company (str): _description_
        location (str): _description_
        salary (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    job = JobListing(title=title, company=company, location=location, salary=salary)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

# Read all job listings (GET)
@app.get("/jobs/")
def get_all_jobs(db: Session = Depends(get_db)):
    """
    Get all job listings from the database.
    
    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
    
    Returns:
        _type_: _description_
    """
    jobs = db.query(JobListing).all()
    return jobs

# Read a specific job listing by ID (GET)
@app.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job listing by ID.
    
    Args:
        job_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    
    Returns:
        _type_: _
        description_
    """
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if job is None:
        return {"error": "Job not found"}
    else: return job
    
#  Update a job listing title by ID (PUT)
@app.put("/jobs/{job_id}")
def update_job(job_id: int, title: str, db: Session = Depends(get_db)):
    """
    Update a job listing by ID.
    
    Args:
        job_id (int): _description_
        title (str): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    
    Returns:
        _type_: _description_
    """
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.title = title
    db.commit()
    return {"message": "Job updated successfully", "updated_job": job}

#  Delete a job listing by ID (DELETE)
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job listing by ID.

    Args:
        job_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    
    Returns:
        _type_: _description_
    """
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}