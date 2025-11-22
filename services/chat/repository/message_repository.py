from sqlmodel import Session, select, func
from typing import Optional, List
from models import Message
from datetime import datetime

class MessageRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, conversation_id: int, sender_id: int, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message
    
    def get_by_id(self, message_id: int) -> Optional[Message]:
        statement = select(Message).where(Message.id == message_id)
        result = self.session.execute(statement)
        return result.scalar_one_or_none()
    
    def get_conversation_messages(self, conversation_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).offset(offset).limit(limit)
        result = self.session.execute(statement)
        messages = result.scalars().all()
        # Return in ascending order (oldest first)
        return list(reversed(messages))
    
    def get_unread_count(self, conversation_id: int, user_id: int) -> int:
        statement = select(func.count(Message.id)).where(
            (Message.conversation_id == conversation_id) &
            (Message.sender_id != user_id) &
            (Message.is_read == False)
        )
        result = self.session.execute(statement)
        return result.scalar() or 0
    
    def mark_as_read(self, message_id: int) -> bool:
        message = self.get_by_id(message_id)
        if not message:
            return False
        
        message.is_read = True
        message.read_at = datetime.utcnow()
        self.session.commit()
        return True
    
    def mark_conversation_as_read(self, conversation_id: int, user_id: int) -> int:
        """Mark all unread messages from other user as read"""
        statement = select(Message).where(
            (Message.conversation_id == conversation_id) &
            (Message.sender_id != user_id) &
            (Message.is_read == False)
        )
        result = self.session.execute(statement)
        messages = result.scalars().all()
        
        count = 0
        for message in messages:
            message.is_read = True
            message.read_at = datetime.utcnow()
            count += 1
        
        self.session.commit()
        return count
    
    def delete(self, message_id: int) -> bool:
        message = self.get_by_id(message_id)
        if not message:
            return False
        
        self.session.delete(message)
        self.session.commit()
        return True
