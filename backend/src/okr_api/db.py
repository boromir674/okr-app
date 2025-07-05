import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@db:5432/okr_db"
)
"""Format is dialect[+driver]://user:password@host/dbname[?key=value..]"""

try:
    engine = create_engine(DATABASE_URL, echo=True)
except Exception as e:
    print(f"Error creating engine with DATABASE_URL {DATABASE_URL}: {e}")
    raise RuntimeError(f"Failed to create engine with DATABASE_URL {DATABASE_URL}: {e}")

print(f"\n\n---- Engine created from URL {DATABASE_URL} with driver: {engine}")  # Debug statement

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

def get_db_session():
    """Provide a synchronous database session.

    Call this to yield a session for database operations.

    Yields:
        Session: A synchronous SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
