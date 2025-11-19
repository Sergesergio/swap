from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os

PAYMENT_DATABASE_URL = os.getenv("PAYMENT_DATABASE_URL", "sqlite:///./payments.db")
engine = create_engine(PAYMENT_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in PAYMENT_DATABASE_URL else {})


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
