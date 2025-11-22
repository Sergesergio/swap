from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://swap_user:swap_password@localhost:5432/notifications")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)


def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
