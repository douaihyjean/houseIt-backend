from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./listings.db"  # Matches your Android SQLite database name

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Metadata (optional, helps with table reflections or migrations if needed later)
metadata = MetaData()
