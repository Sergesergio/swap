from typing import Optional
from pydantic import BaseModel, field_validator

class UserBase(BaseModel):
    email: str
    username: str
    
    @field_validator('email')
    def validate_email_field(cls, v):
        # Simple email validation (check format only)
        if '@' not in v or '.' not in v.split('@')[1]:
            raise ValueError('Invalid email format')
        return v
    
class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    def validate_password_field(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password must be 72 bytes or less')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
class User(UserBase):
    id: int
    is_active: bool = True
    is_verified: bool = False
    
    class Config:
        from_attributes = True