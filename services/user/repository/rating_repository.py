from sqlmodel import Session, select
from typing import Optional, List
from models import Rating

class RatingRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, rating: Rating) -> Rating:
        self.session.add(rating)
        await self.session.commit()
        await self.session.refresh(rating)
        return rating
    
    async def get_by_id(self, rating_id: int) -> Optional[Rating]:
        statement = select(Rating).where(Rating.id == rating_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> List[Rating]:
        statement = select(Rating).where(Rating.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def get_by_user_and_rater(
        self,
        user_id: int,
        rater_id: int
    ) -> Optional[Rating]:
        statement = select(Rating).where(
            Rating.user_id == user_id,
            Rating.rater_id == rater_id
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()