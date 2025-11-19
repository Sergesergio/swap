import sys
import os

# Critical: Fix sys.path BEFORE any other imports to ensure `from shared.*` works
# This is needed because uvicorn subprocess doesn't inherit PYTHONPATH correctly
sys.path.insert(0, '/app')

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING
from jose import jwt, JWTError

from models import UserAuth
from shared.models import UserCreate, User
from shared.exceptions import AuthenticationError, ValidationError
from repository.database import get_session
from repository.user_repository import UserRepository
from utils.auth import (
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_password
)
from events.consumer import AuthEventConsumer
from events.producer import AuthEventProducer
from repository.database import init_db

app = FastAPI(title="Auth Service")

# Initialize event handlers at runtime, not import time
auth_consumer = None
auth_producer = None

@app.on_event("startup")
async def startup_event():
    global auth_consumer, auth_producer
    # Initialize database
    init_db()
    
    try:
        auth_consumer = AuthEventConsumer()
        auth_producer = AuthEventProducer()
        await auth_consumer.start()
        await auth_producer.start()
    except Exception as e:
        print(f"Warning: Failed to initialize Kafka handlers: {e}")
        print("App will continue without event streaming")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        if auth_consumer:
            await auth_consumer.stop()
        if auth_producer:
            await auth_producer.stop()
    except Exception as e:
        print(f"Warning: Error shutting down Kafka handlers: {e}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register", response_model=User)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    repository = UserRepository(session)
    
    # Check if user exists
    if repository.get_by_email(user.email):
        raise ValidationError("Email already registered")
    if repository.get_by_username(user.username):
        raise ValidationError("Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_auth = UserAuth(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    
    return repository.create(user_auth)

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    repository = UserRepository(session)
    user = repository.get_by_email(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise AuthenticationError("Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh")
async def refresh_token(token: str = Depends(oauth2_scheme)):
    try:
        secret = os.getenv("AUTH_SECRET_KEY", "not-secure-local-dev")
        algorithm = os.getenv("AUTH_ALGORITHM", "HS256")
        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise AuthenticationError("Invalid refresh token")
    except JWTError:
        raise AuthenticationError("Invalid refresh token")
    
    access_token = create_access_token(data={"sub": email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        secret = os.getenv("AUTH_SECRET_KEY", "not-secure-local-dev")
        algorithm = os.getenv("AUTH_ALGORITHM", "HS256")
        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise AuthenticationError()
    except JWTError:
        raise AuthenticationError()

    repository = UserRepository(session)
    user = repository.get_by_email(email)
    if not user:
        raise AuthenticationError()
    try:
        print(f"Fetched user object: {user} type={type(user)}")
        if hasattr(user, 'dict'):
            print(f"user.dict(): {user.dict()}")
        elif hasattr(user, '__dict__'):
            print(f"user.__dict__: {user.__dict__}")
    except Exception as e:
        print(f"Error printing user: {e}")
    return user

@app.get("/health")
async def health_check():
    return {"status": "healthy"}