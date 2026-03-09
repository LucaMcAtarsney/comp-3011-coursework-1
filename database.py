# This file is responsible for setting up the database connection.
# It configures the SQLAlchemy engine and provides a session-generating
# function that is used throughout the application to interact with
# the database.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# The database URL is read from the application's settings.
SQLALCHEMY_DATABASE_URL = settings.database_url

# The engine is the entry point to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # `check_same_thread` is only needed for SQLite.
    connect_args={"check_same_thread": False}
)

# A sessionmaker is a factory for creating new Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a class that all of our models will inherit from.
Base = declarative_base()

def get_db():
    """
    A dependency that provides a database session to the API endpoints.
    It ensures that the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
