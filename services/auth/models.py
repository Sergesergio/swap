import sys
import os

# Critical: ensure /app is on sys.path before any local imports
sys.path.insert(0, '/app')

from sqlmodel import SQLModel, Field
from shared.models import UserBase

class UserAuth(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)