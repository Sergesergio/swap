from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os

# Use SQLite for testing, PostgreSQL for production
db_url = os.getenv("DATABASE_URL")
if not db_url or "sqlite" in db_url.lower():
    # Use SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./swap.db")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Use PostgreSQL
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://swap_user:swap_password@postgres:5432/swap")
    engine = create_engine(DATABASE_URL)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLModel Session."""
    with Session(engine) as session:
        yield session


def init_db():
    """Create all tables. Services can call this at startup."""
    SQLModel.metadata.create_all(engine)
