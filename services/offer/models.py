from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from pydantic import constr
import json


class Offer(SQLModel, table=True):
    __tablename__ = "offers"
    
    id: int = Field(default=None, primary_key=True)
    listing_id: int = Field(index=True)
    buyer_id: int = Field(index=True)
    seller_id: int = Field(index=True)
    status: str = Field(default="pending")  # pending, accepted, rejected, cancelled
    type: str  # direct_buy, swap
    price: Optional[float] = Field(default=None)
    swap_listing_ids: Optional[str] = Field(default=None)  # JSON string
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class OfferMessage(SQLModel, table=True):
    __tablename__ = "offer_messages"
    
    id: int = Field(default=None, primary_key=True)
    offer_id: int = Field(foreign_key="offers.id", index=True)
    sender_id: int = Field(index=True)
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Request Models
class OfferCreate(SQLModel):
    listing_id: int
    buyer_id: int
    seller_id: int
    type: str
    price: Optional[float] = None
    swap_listing_ids: Optional[List[int]] = None
    message: Optional[str] = None
    expires_at: Optional[datetime] = None


class MessageCreate(SQLModel):
    message: constr(min_length=1, max_length=1000)


# Response Models
class OfferResponse(SQLModel):
    id: int
    listing_id: int
    buyer_id: int
    seller_id: int
    status: str
    type: str
    price: Optional[float]
    swap_listing_ids: Optional[List[int]]
    message: Optional[str]
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime]


# Compatibility aliases / additional models expected by routers
class OfferRead(OfferResponse):
    pass


class OfferUpdate(SQLModel):
    status: Optional[str] = None
    price: Optional[float] = None
    message: Optional[str] = None
    expires_at: Optional[datetime] = None
    swap_listing_ids: Optional[List[int]] = None


class OfferMessageCreate(SQLModel):
    message: constr(min_length=1, max_length=1000)


class OfferMessageRead(SQLModel):
    id: int
    offer_id: int
    sender_id: int
    message: str
    created_at: datetime