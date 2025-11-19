from sqlmodel import Session, select
from typing import Optional, List
from models import Listing, ListingImage, ListingTag
from datetime import datetime

class ListingRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def create(
        self,
        listing: Listing,
        images: List[str] = None,
        tags: List[str] = None
    ) -> Listing:
        self.session.add(listing)
        await self.session.commit()
        await self.session.refresh(listing)
        
        # Add images if provided
        if images:
            for idx, image_url in enumerate(images):
                image = ListingImage(
                    listing_id=listing.id,
                    image_url=image_url,
                    is_primary=(idx == 0)
                )
                self.session.add(image)
        
        # Add tags if provided
        if tags:
            for tag_name in tags:
                tag = ListingTag(
                    listing_id=listing.id,
                    name=tag_name
                )
                self.session.add(tag)
        
        await self.session.commit()
        return listing
    
    async def get_by_id(self, listing_id: int) -> Optional[Listing]:
        statement = select(Listing).where(Listing.id == listing_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> List[Listing]:
        statement = select(Listing).where(
            Listing.user_id == user_id,
            Listing.status != "deleted"
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def get_by_category(self, category_id: int) -> List[Listing]:
        statement = select(Listing).where(
            Listing.category_id == category_id,
            Listing.status == "active"
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def search(
        self,
        query: str = None,
        category_id: int = None,
        min_price: float = None,
        max_price: float = None,
        condition: str = None
    ) -> List[Listing]:
        statement = select(Listing).where(Listing.status == "active")
        
        if query:
            statement = statement.where(
                (Listing.title.ilike(f"%{query}%")) |
                (Listing.description.ilike(f"%{query}%"))
            )
        
        if category_id:
            statement = statement.where(Listing.category_id == category_id)
        
        if min_price is not None:
            statement = statement.where(Listing.price >= min_price)
        
        if max_price is not None:
            statement = statement.where(Listing.price <= max_price)
        
        if condition:
            statement = statement.where(Listing.condition == condition)
        
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def update(self, listing_id: int, listing_update: Listing) -> Optional[Listing]:
        listing = await self.get_by_id(listing_id)
        if not listing:
            return None
        
        for key, value in listing_update.dict(exclude_unset=True).items():
            setattr(listing, key, value)
        
        listing.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(listing)
        return listing
    
    async def delete(self, listing_id: int) -> bool:
        listing = await self.get_by_id(listing_id)
        if not listing:
            return False
        
        listing.status = "deleted"
        listing.updated_at = datetime.utcnow()
        await self.session.commit()
        return True
    
    async def increment_views(self, listing_id: int) -> bool:
        listing = await self.get_by_id(listing_id)
        if not listing:
            return False
        
        listing.views += 1
        await self.session.commit()
        return True