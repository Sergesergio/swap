from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from datetime import datetime
from typing import List

from models import Profile, Wallet, Rating
from repository.database import get_session
from repository.profile_repository import ProfileRepository
from repository.wallet_repository import WalletRepository
from repository.rating_repository import RatingRepository
from shared.exceptions import ResourceNotFound, ValidationError
from events.consumer import UserEventConsumer
from events.producer import UserEventProducer

app = FastAPI(title="User Service")

# Initialize event handlers
user_consumer = UserEventConsumer()
user_producer = UserEventProducer()

@app.on_event("startup")
async def startup_event():
    await user_consumer.start()
    await user_producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await user_consumer.stop()
    await user_producer.stop()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/profiles", response_model=Profile)
async def create_profile(
    profile: Profile,
    session: Session = Depends(get_session)
):
    repository = ProfileRepository(session)
    return await repository.create(profile)

@app.get("/profiles/{user_id}", response_model=Profile)
async def get_profile(
    user_id: int,
    session: Session = Depends(get_session)
):
    repository = ProfileRepository(session)
    profile = await repository.get_by_user_id(user_id)
    if not profile:
        raise ResourceNotFound(f"Profile not found for user {user_id}")
    return profile

@app.put("/profiles/{user_id}", response_model=Profile)
async def update_profile(
    user_id: int,
    profile_update: Profile,
    session: Session = Depends(get_session)
):
    repository = ProfileRepository(session)
    profile = await repository.get_by_user_id(user_id)
    if not profile:
        raise ResourceNotFound(f"Profile not found for user {user_id}")
    
    return await repository.update(profile.id, profile_update)

@app.get("/wallets/{user_id}", response_model=Wallet)
async def get_wallet(
    user_id: int,
    session: Session = Depends(get_session)
):
    repository = WalletRepository(session)
    wallet = await repository.get_by_user_id(user_id)
    if not wallet:
        wallet = Wallet(user_id=user_id)
        wallet = await repository.create(wallet)
    return wallet

@app.post("/ratings", response_model=Rating)
async def create_rating(
    rating: Rating,
    session: Session = Depends(get_session)
):
    if rating.user_id == rating.rater_id:
        raise ValidationError("Users cannot rate themselves")
    
    repository = RatingRepository(session)
    profile_repo = ProfileRepository(session)
    
    # Check if user has already rated
    existing_rating = await repository.get_by_user_and_rater(
        rating.user_id,
        rating.rater_id
    )
    if existing_rating:
        raise ValidationError("User has already rated this profile")
    
    # Create rating
    new_rating = await repository.create(rating)
    
    # Update profile rating
    profile = await profile_repo.get_by_user_id(rating.user_id)
    if profile:
        total_ratings = profile.total_ratings + 1
        new_rating_value = (
            (profile.rating * profile.total_ratings) + rating.rating
        ) / total_ratings
        
        await profile_repo.update(
            profile.id,
            Profile(
                rating=new_rating_value,
                total_ratings=total_ratings,
                updated_at=datetime.utcnow()
            )
        )
    
    return new_rating

@app.get("/ratings/{user_id}", response_model=List[Rating])
async def get_user_ratings(
    user_id: int,
    session: Session = Depends(get_session)
):
    repository = RatingRepository(session)
    return await repository.get_by_user_id(user_id)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}