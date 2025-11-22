from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import constr

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: int = Field(default=None, primary_key=True)
    user1_id: int = Field(index=True)
    user2_id: int = Field(index=True)
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    sender_id: int = Field(index=True)
    content: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

class ConversationResponse(SQLModel):
    id: int
    user1_id: int
    user2_id: int
    last_message: Optional[str]
    last_message_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    unread_count: int = 0

class MessageResponse(SQLModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime]

class MessageCreate(SQLModel):
    content: constr(min_length=1, max_length=5000)

class ConversationCreate(SQLModel):
    user1_id: int
    user2_id: int
