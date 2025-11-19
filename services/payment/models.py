from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: int = Field(default=None, primary_key=True)
    offer_id: int = Field(index=True)
    amount: float
    status: str = Field(default="held")  # held, released
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentHoldRequest(SQLModel):
    offer_id: int
    amount: float

class PaymentResponse(SQLModel):
    id: int
    offer_id: int
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime
