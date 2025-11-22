from sqlmodel import Session, select
from typing import Optional, List
from models import Conversation, Message
from datetime import datetime

class ConversationRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user1_id: int, user2_id: int) -> Conversation:
        # Ensure consistent ordering (smaller ID first)
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id
        
        # Check if conversation already exists
        existing = self.get_by_users(user1_id, user2_id)
        if existing:
            return existing
        
        conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation
    
    def get_by_id(self, conversation_id: int) -> Optional[Conversation]:
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    def get_by_users(self, user1_id: int, user2_id: int) -> Optional[Conversation]:
        # Normalize user IDs
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id
        
        statement = select(Conversation).where(
            (Conversation.user1_id == user1_id) & (Conversation.user2_id == user2_id),
            Conversation.is_active == True
        )
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    def get_user_conversations(self, user_id: int) -> List[Conversation]:
        statement = select(Conversation).where(
            ((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)),
            Conversation.is_active == True
        ).order_by(Conversation.last_message_at.desc())
        result = self.session.execute(statement)
        return result.scalars().all()
    
    def update_last_message(self, conversation_id: int, message: str) -> Conversation:
        conversation = self.get_by_id(conversation_id)
        if not conversation:
            return None
        
        conversation.last_message = message
        conversation.last_message_at = datetime.utcnow()
        conversation.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(conversation)
        return conversation
    
    def deactivate(self, conversation_id: int) -> bool:
        conversation = self.get_by_id(conversation_id)
        if not conversation:
            return False
        
        conversation.is_active = False
        conversation.updated_at = datetime.utcnow()
        self.session.commit()
        return True
