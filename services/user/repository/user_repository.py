"""
Unified User Repository combining profile, wallet, and rating operations
"""
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional
from models import Profile, Wallet, Rating
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    """Unified repository for user-related operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create_profile(self, user_id: int, display_name: str = None) -> Profile:
        """Create initial user profile"""
        profile = Profile(
            user_id=user_id,
            display_name=display_name or f"User {user_id}",
            bio="",
            rating=0.0,
            total_ratings=0,
            is_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile
    
    async def create_wallet(self, user_id: int) -> Wallet:
        """Create initial wallet for user"""
        wallet = Wallet(
            user_id=user_id,
            balance=0.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(wallet)
        self.session.commit()
        self.session.refresh(wallet)
        return wallet
    
    async def update_verification_status(self, user_id: int, is_verified: bool) -> Optional[Profile]:
        """Update user verification status"""
        statement = select(Profile).where(Profile.user_id == user_id)
        profile = self.session.exec(statement).first()
        
        if profile:
            profile.is_verified = is_verified
            profile.updated_at = datetime.utcnow()
            self.session.add(profile)
            self.session.commit()
            self.session.refresh(profile)
        
        return profile
    
    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        """Get profile by user ID"""
        statement = select(Profile).where(Profile.user_id == user_id)
        return self.session.exec(statement).first()
