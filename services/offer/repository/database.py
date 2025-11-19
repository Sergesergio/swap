from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os

OFFER_DATABASE_URL = os.getenv("OFFER_DATABASE_URL", "sqlite:///./offers.db")
engine = create_engine(OFFER_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in OFFER_DATABASE_URL else {})


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)