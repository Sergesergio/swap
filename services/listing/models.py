from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from pydantic import constr

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Listing(SQLModel, table=True):
    __tablename__ = "listings"
    
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    price: float = Field(ge=0)
    category_id: int = Field(foreign_key="categories.id")
    user_id: int = Field(index=True)
    status: str = Field(default="active")  # active, sold, deleted
    condition: str  # new, like_new, good, fair, poor
    location: str
    is_negotiable: bool = Field(default=True)
    views: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ListingImage(SQLModel, table=True):
    __tablename__ = "listing_images"
    
    id: int = Field(default=None, primary_key=True)
    listing_id: int = Field(foreign_key="listings.id")
    image_url: str
    is_primary: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ListingTag(SQLModel, table=True):
    __tablename__ = "listing_tags"
    
    id: int = Field(default=None, primary_key=True)
    listing_id: int = Field(foreign_key="listings.id")
    name: constr(min_length=1, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Response Models
class ListingResponse(SQLModel):
    id: int
    title: str
    description: str
    price: float
    category_id: int
    user_id: int
    status: str
    condition: str
    location: str
    is_negotiable: bool
    views: int
    created_at: datetime
    updated_at: datetime
    images: List[str] = []
    tags: List[str] = []

# Request Models
class ListingCreate(SQLModel):
    title: str
    description: str
    price: float
    category_id: int
    condition: str
    location: str
    is_negotiable: bool = True
    tags: List[str] = []