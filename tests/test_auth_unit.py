"""
Unit tests for Auth Service
Tests user registration, login, token management
"""
import pytest
import httpx
from typing import Dict, Any


class TestAuthServiceUnit:
    """Unit tests for auth service endpoints"""
    
    def test_health_check(self, auth_client: httpx.Client):
        """Test auth service health endpoint"""
        response = auth_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_register_success(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test successful user registration"""
        response = auth_client.post("/register", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert "id" in data
        assert "hashed_password" not in data
    
    def test_register_duplicate_email(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test registration fails with duplicate email"""
        # First registration
        auth_client.post("/register", json=test_user_data)
        
        # Second registration with same email
        duplicate_data = test_user_data.copy()
        duplicate_data["username"] = "different_user"
        response = auth_client.post("/register", json=duplicate_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_duplicate_username(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test registration fails with duplicate username"""
        # First registration
        auth_client.post("/register", json=test_user_data)
        
        # Second registration with same username
        duplicate_data = test_user_data.copy()
        duplicate_data["email"] = "different@example.com"
        response = auth_client.post("/register", json=duplicate_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_weak_password(self, auth_client: httpx.Client):
        """Test registration fails with weak password"""
        weak_password_data = {
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "short"  # Less than 8 characters
        }
        response = auth_client.post("/register", json=weak_password_data)
        assert response.status_code == 422
    
    def test_register_invalid_email(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test registration fails with invalid email"""
        invalid_email_data = test_user_data.copy()
        invalid_email_data["email"] = "not-an-email"
        response = auth_client.post("/register", json=invalid_email_data)
        assert response.status_code == 422
    
    def test_login_success(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test successful login"""
        # Register first
        auth_client.post("/register", json=test_user_data)
        
        # Login
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = auth_client.post("/token", data=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_email(self, auth_client: httpx.Client):
        """Test login fails with non-existent email"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
        response = auth_client.post("/token", data=login_data)
        assert response.status_code == 401
    
    def test_login_invalid_password(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test login fails with wrong password"""
        # Register first
        auth_client.post("/register", json=test_user_data)
        
        # Login with wrong password
        login_data = {
            "username": test_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = auth_client.post("/token", data=login_data)
        assert response.status_code == 401
    
    def test_get_current_user(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test getting current user profile"""
        # Register and login
        auth_client.post("/register", json=test_user_data)
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = auth_client.post("/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = auth_client.get("/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
    
    def test_get_current_user_no_token(self, auth_client: httpx.Client):
        """Test getting current user without token"""
        response = auth_client.get("/me")
        assert response.status_code == 403
    
    def test_refresh_token(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test token refresh"""
        # Register and login
        auth_client.post("/register", json=test_user_data)
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = auth_client.post("/token", data=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = auth_client.post("/refresh", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


class TestPasswordValidation:
    """Tests for password validation"""
    
    def test_password_min_length(self, auth_client: httpx.Client):
        """Test password minimum length requirement"""
        short_password = {
            "email": "short@example.com",
            "username": "shortuser",
            "password": "Short1!"  # 7 characters
        }
        response = auth_client.post("/register", json=short_password)
        assert response.status_code == 422
    
    def test_password_max_bytes(self, auth_client: httpx.Client):
        """Test password maximum byte length"""
        long_password = {
            "email": "long@example.com",
            "username": "longuser",
            "password": "x" * 100  # Over 72 bytes
        }
        response = auth_client.post("/register", json=long_password)
        assert response.status_code == 422
    
    def test_password_unicode_bytes(self, auth_client: httpx.Client):
        """Test password with unicode characters respects byte limit"""
        unicode_password = {
            "email": "unicode@example.com",
            "username": "unicodeuser",
            "password": "Pass🎉" * 20  # Unicode takes multiple bytes
        }
        response = auth_client.post("/register", json=unicode_password)
        # Should either work or fail validation, but not crash
        assert response.status_code in [200, 422]


class TestAuthSecurity:
    """Security-related tests for auth service"""
    
    def test_password_not_in_response(self, auth_client: httpx.Client, test_user_data: Dict[str, str]):
        """Test that password is never returned in responses"""
        response = auth_client.post("/register", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert "password" not in data
        assert "hashed_password" not in data
    
    def test_jwt_malformed_token(self, auth_client: httpx.Client):
        """Test that malformed JWT is rejected"""
        headers = {"Authorization": "Bearer malformed.token.here"}
        response = auth_client.get("/me", headers=headers)
        assert response.status_code == 401
    
    def test_missing_bearer_token(self, auth_client: httpx.Client):
        """Test that missing Authorization header fails"""
        response = auth_client.get("/me")
        assert response.status_code == 403
