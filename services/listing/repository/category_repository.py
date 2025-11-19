from sqlmodel import Session, select
from typing import Optional, List
from models import Category

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        statement = select(Category).where(Category.id == category_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[Category]:
        statement = select(Category)
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def get_by_parent_id(self, parent_id: int) -> List[Category]:
        statement = select(Category).where(Category.parent_id == parent_id)
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def update(self, category_id: int, category_update: Category) -> Optional[Category]:
        category = await self.get_by_id(category_id)
        if not category:
            return None
        
        for key, value in category_update.dict(exclude_unset=True).items():
            setattr(category, key, value)
        
        await self.session.commit()
        await self.session.refresh(category)
        return category
    
    async def delete(self, category_id: int) -> bool:
        category = await self.get_by_id(category_id)
        if not category:
            return False
        
        await self.session.delete(category)
        await self.session.commit()
        return True