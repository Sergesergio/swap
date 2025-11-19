import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
import os

from services.offer.main import app as offer_app
from services.payment.main import app as payment_app
from shared.auth import get_current_user, User
from services.offer.repository import database as offer_db
from services.payment.repository import database as payment_db


# Setup in-memory SQLite for all tests
@pytest.fixture(scope="session", autouse=True)
def setup_test_databases():
    """Setup in-memory SQLite for all tests"""
    # Create in-memory engines
    offer_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    payment_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    
    # Override the module-level engines
    offer_db.engine = offer_engine
    payment_db.engine = payment_engine
    
    # Create all tables
    SQLModel.metadata.create_all(offer_engine)
    SQLModel.metadata.create_all(payment_engine)
    
    yield


# Mock current user for testing
def get_test_user():
    return User(id=1, email="buyer@example.com", username="buyer")


def get_test_seller():
    return User(id=2, email="seller@example.com", username="seller")


# Override dependencies
offer_app.dependency_overrides[get_current_user] = get_test_user
payment_app.dependency_overrides[get_current_user] = get_test_user


@pytest.mark.asyncio
async def test_create_offer():
    """Test creating a new offer"""
    client = TestClient(offer_app)
    offer_data = {
        "listing_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "type": "direct_buy",
        "price": 100.0,
        "message": "I want to buy this item"
    }
    
    response = client.post("/api/v1/offers/", json=offer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["type"] == "direct_buy"
    assert data["price"] == 100.0


@pytest.mark.asyncio
async def test_get_offer():
    """Test retrieving an offer"""
    client = TestClient(offer_app)
    # First create an offer
    offer_data = {
        "listing_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "type": "direct_buy",
        "price": 100.0
    }
    
    create_response = client.post("/api/v1/offers/", json=offer_data)
    offer_id = create_response.json()["id"]
    
    # Retrieve it
    get_response = client.get(f"/api/v1/offers/{offer_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == offer_id


@pytest.mark.asyncio
async def test_accept_offer_with_payment():
    """Test accepting an offer, which should trigger payment hold"""
    client = TestClient(offer_app)
    # Create offer as buyer
    offer_data = {
        "listing_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "type": "direct_buy",
        "price": 100.0
    }
    create_response = client.post("/api/v1/offers/", json=offer_data)
    offer_id = create_response.json()["id"]
    
    # Override to seller for accepting
    offer_app.dependency_overrides[get_current_user] = get_test_seller
    
    # Accept offer
    accept_response = client.post(f"/api/v1/offers/{offer_id}/accept")
    assert accept_response.status_code == 200
    assert accept_response.json()["status"] == "accepted"
    
    # Reset override
    offer_app.dependency_overrides[get_current_user] = get_test_user


@pytest.mark.asyncio
async def test_reject_offer():
    """Test rejecting an offer"""
    client = TestClient(offer_app)
    # Create offer
    offer_data = {
        "listing_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "type": "direct_buy",
        "price": 100.0
    }
    create_response = client.post("/api/v1/offers/", json=offer_data)
    offer_id = create_response.json()["id"]
    
    # Override to seller
    offer_app.dependency_overrides[get_current_user] = get_test_seller
    
    # Reject offer
    reject_response = client.post(f"/api/v1/offers/{offer_id}/reject")
    assert reject_response.status_code == 200
    assert reject_response.json()["status"] == "rejected"
    
    # Reset override
    offer_app.dependency_overrides[get_current_user] = get_test_user


@pytest.mark.asyncio
async def test_add_offer_message():
    """Test adding a message to an offer"""
    client = TestClient(offer_app)
    # Create offer
    offer_data = {
        "listing_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "type": "direct_buy",
        "price": 100.0
    }
    create_response = client.post("/api/v1/offers/", json=offer_data)
    offer_id = create_response.json()["id"]
    
    # Add message
    message_data = {"message": "Is this item still available?"}
    msg_response = client.post(
        f"/api/v1/offers/{offer_id}/messages/",
        json=message_data
    )
    assert msg_response.status_code == 200
    assert msg_response.json()["message"] == "Is this item still available?"


@pytest.mark.asyncio
async def test_get_offer_messages():
    """Test retrieving messages for an offer"""
    client = TestClient(offer_app)
    # Create offer
    offer_data = {
        "listing_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "type": "direct_buy",
        "price": 100.0
    }
    create_response = client.post("/api/v1/offers/", json=offer_data)
    offer_id = create_response.json()["id"]
    
    # Add message
    message_data = {"message": "Test message"}
    client.post(f"/api/v1/offers/{offer_id}/messages/", json=message_data)
    
    # Get messages
    msg_response = client.get(f"/api/v1/offers/{offer_id}/messages/")
    assert msg_response.status_code == 200
    messages = msg_response.json()
    assert len(messages) > 0


@pytest.mark.asyncio
async def test_payment_hold():
    """Test payment hold endpoint"""
    client = TestClient(payment_app)
    payment_data = {
        "offer_id": 1,
        "amount": 100.0
    }
    
    response = client.post("/api/v1/payments/hold", json=payment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "held"
    assert data["amount"] == 100.0


@pytest.mark.asyncio
async def test_payment_release():
    """Test payment release endpoint"""
    client = TestClient(payment_app)
    # Hold payment first
    payment_data = {"offer_id": 1, "amount": 100.0}
    hold_response = client.post("/api/v1/payments/hold", json=payment_data)
    payment_id = hold_response.json()["id"]
    
    # Release payment
    release_response = client.post(f"/api/v1/payments/{payment_id}/release")
    assert release_response.status_code == 200
    assert release_response.json()["status"] == "released"


@pytest.mark.asyncio
async def test_get_user_offers():
    """Test retrieving offers for a user"""
    client = TestClient(offer_app)
    # Create multiple offers
    for i in range(3):
        offer_data = {
            "listing_id": i + 1,
            "buyer_id": 1,
            "seller_id": 2,
            "type": "direct_buy",
            "price": 100.0 + i
        }
        client.post("/api/v1/offers/", json=offer_data)
    
    # Get user offers
    response = client.get("/api/v1/offers/user/1")
    assert response.status_code == 200
    offers = response.json()
    assert len(offers) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
