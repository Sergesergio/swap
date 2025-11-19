from sqlmodel import Session, select
from typing import Optional
from models import Profile

class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, profile: Profile) -> Profile:
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile
    
    async def get_by_id(self, profile_id: int) -> Optional[Profile]:
        statement = select(Profile).where(Profile.id == profile_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        statement = select(Profile).where(Profile.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def update(self, profile_id: int, profile_update: Profile) -> Profile:
        profile = await self.get_by_id(profile_id)
        if not profile:
            return None
        
        for key, value in profile_update.dict(exclude_unset=True).items():
            setattr(profile, key, value)
        
        await self.session.commit()
        await self.session.refresh(profile)
        return profile