"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from .config import settings

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using
    pool_size=5,
    max_overflow=10,
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db() -> Generator:
    """Get database session.

    Dependency for FastAPI endpoints that provides a database session
    and ensures it's properly closed after the request.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
