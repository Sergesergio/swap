from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os

DATABASE_URL = os.getenv("LISTING_DATABASE_URL", "postgresql://swap_user:swap_password@postgres:5432/listings")

engine = create_engine(DATABASE_URL)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)