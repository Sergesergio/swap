from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime

from models import Conversation, Message, ConversationResponse, MessageResponse, MessageCreate, ConversationCreate
from repository.database import get_session, init_db
from repository.conversation_repository import ConversationRepository
from repository.message_repository import MessageRepository
from shared.exceptions import ResourceNotFound, ValidationError
from events.consumer import ChatEventConsumer
from events.producer import ChatEventProducer

app = FastAPI(title="Chat Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chat_consumer = None
chat_producer = None

@app.on_event("startup")
async def startup_event():
    global chat_consumer, chat_producer
    
    # Initialize database tables
    init_db()
    
    # Start event handlers (create them now in async context)
    chat_consumer = ChatEventConsumer()
    chat_producer = ChatEventProducer()
    await chat_consumer.start()
    await chat_producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await chat_consumer.stop()
    await chat_producer.stop()

# Conversation endpoints
@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conv_create: ConversationCreate,
    session: Session = Depends(get_session)
):
    """Create or get existing conversation between two users"""
    if conv_create.user1_id == conv_create.user2_id:
        raise ValidationError("Cannot create conversation with yourself")
    
    repository = ConversationRepository(session)
    conversation = repository.create(conv_create.user1_id, conv_create.user2_id)
    
    # Publish event
    await chat_producer.conversation_created(conv_create.user1_id, conv_create.user2_id)
    
    return ConversationResponse(
        **conversation.dict(),
        unread_count=0
    )

@app.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    user_id: int = Query(...),
    session: Session = Depends(get_session)
):
    """Get all conversations for a user"""
    repository = ConversationRepository(session)
    conversations = repository.get_user_conversations(user_id)
    
    message_repo = MessageRepository(session)
    result = []
    for conv in conversations:
        unread_count = message_repo.get_unread_count(conv.id, user_id)
        result.append(ConversationResponse(
            **conv.dict(),
            unread_count=unread_count
        ))
    
    return result

@app.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    user_id: int = Query(...),
    session: Session = Depends(get_session)
):
    """Get specific conversation"""
    repository = ConversationRepository(session)
    conversation = repository.get_by_id(conversation_id)
    if not conversation:
        raise ResourceNotFound(f"Conversation {conversation_id} not found")
    
    # Verify user is part of conversation
    if user_id not in [conversation.user1_id, conversation.user2_id]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    message_repo = MessageRepository(session)
    unread_count = message_repo.get_unread_count(conversation_id, user_id)
    
    return ConversationResponse(
        **conversation.dict(),
        unread_count=unread_count
    )

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    user_id: int = Query(...),
    session: Session = Depends(get_session)
):
    """Deactivate/delete conversation"""
    repository = ConversationRepository(session)
    conversation = repository.get_by_id(conversation_id)
    if not conversation:
        raise ResourceNotFound(f"Conversation {conversation_id} not found")
    
    # Verify user is part of conversation
    if user_id not in [conversation.user1_id, conversation.user2_id]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    success = repository.deactivate(conversation_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete conversation")
    
    return {"message": "Conversation deleted successfully"}

# Message endpoints
@app.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    msg_create: MessageCreate,
    sender_id: int = Query(...),
    session: Session = Depends(get_session)
):
    """Send message in conversation"""
    conv_repo = ConversationRepository(session)
    conversation = conv_repo.get_by_id(conversation_id)
    if not conversation:
        raise ResourceNotFound(f"Conversation {conversation_id} not found")
    
    # Verify sender is part of conversation
    if sender_id not in [conversation.user1_id, conversation.user2_id]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    msg_repo = MessageRepository(session)
    message = msg_repo.create(conversation_id, sender_id, msg_create.content)
    
    # Update conversation's last message
    conv_repo.update_last_message(conversation_id, msg_create.content)
    
    # Publish event
    await chat_producer.message_sent(
        conversation_id=conversation_id,
        sender_id=sender_id,
        data={"content": msg_create.content}
    )
    
    return MessageResponse(**message.dict())

@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    user_id: int = Query(...),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    """Get messages in conversation"""
    conv_repo = ConversationRepository(session)
    conversation = conv_repo.get_by_id(conversation_id)
    if not conversation:
        raise ResourceNotFound(f"Conversation {conversation_id} not found")
    
    # Verify user is part of conversation
    if user_id not in [conversation.user1_id, conversation.user2_id]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    msg_repo = MessageRepository(session)
    messages = msg_repo.get_conversation_messages(conversation_id, limit, offset)
    
    return [MessageResponse(**msg.dict()) for msg in messages]

@app.post("/messages/{message_id}/read")
async def mark_message_read(
    message_id: int,
    user_id: int = Query(...),
    session: Session = Depends(get_session)
):
    """Mark message as read"""
    msg_repo = MessageRepository(session)
    message = msg_repo.get_by_id(message_id)
    if not message:
        raise ResourceNotFound(f"Message {message_id} not found")
    
    # Verify user can read this message
    conv_repo = ConversationRepository(session)
    conversation = conv_repo.get_by_id(message.conversation_id)
    if user_id not in [conversation.user1_id, conversation.user2_id]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    success = msg_repo.mark_as_read(message_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to mark message as read")
    
    return {"message": "Message marked as read"}

@app.post("/conversations/{conversation_id}/read")
async def mark_conversation_read(
    conversation_id: int,
    user_id: int = Query(...),
    session: Session = Depends(get_session)
):
    """Mark all messages in conversation as read"""
    conv_repo = ConversationRepository(session)
    conversation = conv_repo.get_by_id(conversation_id)
    if not conversation:
        raise ResourceNotFound(f"Conversation {conversation_id} not found")
    
    # Verify user is part of conversation
    if user_id not in [conversation.user1_id, conversation.user2_id]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    msg_repo = MessageRepository(session)
    count = msg_repo.mark_conversation_as_read(conversation_id, user_id)
    
    return {"message": f"Marked {count} messages as read"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
