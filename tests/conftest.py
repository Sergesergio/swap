"""
Pytest configuration and shared fixtures for all tests
"""
import pytest
import os
import sys
from typing import Generator

# Add app root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
import httpx


# Use SQLite in-memory for tests
@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="auth_client")
def auth_client_fixture():
    """HTTP client for auth service"""
    return httpx.Client(base_url="http://localhost:8000", timeout=30.0)


@pytest.fixture(name="user_client")
def user_client_fixture():
    """HTTP client for user service"""
    return httpx.Client(base_url="http://localhost:8001", timeout=30.0)


@pytest.fixture(name="listing_client")
def listing_client_fixture():
    """HTTP client for listing service"""
    return httpx.Client(base_url="http://localhost:8002", timeout=30.0)


@pytest.fixture(name="offer_client")
def offer_client_fixture():
    """HTTP client for offer service"""
    return httpx.Client(base_url="http://localhost:8003", timeout=30.0)


@pytest.fixture(name="payment_client")
def payment_client_fixture():
    """HTTP client for payment service"""
    return httpx.Client(base_url="http://localhost:8004", timeout=30.0)


@pytest.fixture
def test_user_data():
    """Test user credentials"""
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "SecurePassword123!"
    }


@pytest.fixture
def test_seller_data():
    """Test seller credentials"""
    return {
        "email": "seller@example.com",
        "username": "seller",
        "password": "SellerPass123!"
    }


@pytest.fixture
def test_listing_data():
    """Test listing data"""
    return {
        "title": "Vintage Leather Jacket",
        "description": "Classic brown leather jacket in excellent condition",
        "category": "fashion",
        "condition": "excellent",
        "price": 150.0,
        "images": ["https://example.com/image1.jpg"]
    }


@pytest.fixture
def test_offer_data():
    """Test offer data"""
    return {
        "listing_id": 1,
        "type": "direct_buy",
        "price": 150.0,
        "message": "I'm interested in buying this item"
    }


@pytest.fixture
def test_payment_data():
    """Test payment data"""
    return {
        "offer_id": 1,
        "amount": 150.0,
        "payment_method": "credit_card"
    }
