from sqlmodel import Session, select
from typing import Optional, List
from models import Category

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        statement = select(Category).where(Category.id == category_id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    def get_all(self) -> List[Category]:
        statement = select(Category)
        result = self.session.execute(statement)
        return result.scalars().all()
    
    def get_by_parent_id(self, parent_id: int) -> List[Category]:
        statement = select(Category).where(Category.parent_id == parent_id)
        result = self.session.execute(statement)
        return result.scalars().all()
    
    def update(self, category_id: int, category_update: Category) -> Optional[Category]:
        category = self.get_by_id(category_id)
        if not category:
            return None
        
        for key, value in category_update.dict(exclude_unset=True).items():
            setattr(category, key, value)
        
        self.session.commit()
        self.session.refresh(category)
        return category
    
    def delete(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        
        self.session.delete(category)
        self.session.commit()
        return True