from sqlmodel import Session, select
from typing import Optional
from models import UserAuth

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user: UserAuth) -> UserAuth:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_by_email(self, email: str) -> Optional[UserAuth]:
        statement = select(UserAuth).where(UserAuth.email == email)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    def get_by_username(self, username: str) -> Optional[UserAuth]:
        statement = select(UserAuth).where(UserAuth.username == username)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    def get_by_id(self, user_id: int) -> Optional[UserAuth]:
        statement = select(UserAuth).where(UserAuth.id == user_id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()