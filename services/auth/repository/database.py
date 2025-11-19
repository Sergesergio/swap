from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os

DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "postgresql://swap_user:swap_password@postgres:5432/auth")

engine = create_engine(DATABASE_URL)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def init_db():
    # Import models to register them with SQLModel metadata
    from models import UserAuth
    SQLModel.metadata.create_all(engine)