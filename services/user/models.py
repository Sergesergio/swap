from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True, index=True)
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_verified_seller: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    rating: float = Field(default=0.0)
    total_ratings: int = Field(default=0)

class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"
    
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True, index=True)
    balance: float = Field(default=0.0)
    locked_balance: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Rating(SQLModel, table=True):
    __tablename__ = "ratings"
    
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    rater_id: int = Field(index=True)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)