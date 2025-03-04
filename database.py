from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - Format: postgresql://username:password@host/database_name
DATABASE_URL = "postgresql://postgres:yourpassword@localhost/joblistings_db"

# Create a SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# Create a session factory that will be used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for defining SQLAlchemy declarative models
Base = declarative_base()