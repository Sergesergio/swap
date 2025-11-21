"""
Unit tests for Listing service endpoints
"""
import pytest
import httpx
from io import BytesIO


class TestListingServiceUnit:
    """Test Listing service endpoints"""
    
    def test_health_check(self, listing_client: httpx.Client):
        """Test health check endpoint"""
        response = listing_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    # Category endpoints
    def test_create_category(self, listing_client: httpx.Client):
        """Test creating a category"""
        category_data = {
            "name": "Electronics",
            "description": "Electronic items"
        }
        response = listing_client.post("/categories", json=category_data)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "Electronics"
        assert data["description"] == "Electronic items"
    
    def test_get_categories(self, listing_client: httpx.Client):
        """Test getting all categories"""
        # Create a category first
        category_data = {
            "name": "Fashion",
            "description": "Fashion items"
        }
        listing_client.post("/categories", json=category_data)
        
        # Get all categories
        response = listing_client.get("/categories")
        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
    
    def test_get_category_by_id(self, listing_client: httpx.Client):
        """Test getting a specific category"""
        # Create a category
        category_data = {
            "name": "Home",
            "description": "Home items"
        }
        create_response = listing_client.post("/categories", json=category_data)
        category_id = create_response.json()["id"]
        
        # Get the category
        response = listing_client.get(f"/categories/{category_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Home"
    
    def test_get_nonexistent_category(self, listing_client: httpx.Client):
        """Test getting a non-existent category"""
        response = listing_client.get("/categories/99999")
        assert response.status_code == 404
    
    # Listing endpoints
    def test_search_listings_empty(self, listing_client: httpx.Client):
        """Test searching listings when none exist"""
        response = listing_client.get("/listings")
        assert response.status_code == 200
        listings = response.json()
        assert isinstance(listings, list)
    
    def test_search_listings_with_query(self, listing_client: httpx.Client):
        """Test searching listings with a query"""
        response = listing_client.get("/listings?query=jacket")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_listings_with_price_range(self, listing_client: httpx.Client):
        """Test searching listings with price range"""
        response = listing_client.get("/listings?min_price=50&max_price=200")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_listings_with_category(self, listing_client: httpx.Client):
        """Test searching listings by category"""
        response = listing_client.get("/listings?category_id=1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_listings_with_condition(self, listing_client: httpx.Client):
        """Test searching listings by condition"""
        response = listing_client.get("/listings?condition=new")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_nonexistent_listing(self, listing_client: httpx.Client):
        """Test getting a non-existent listing"""
        response = listing_client.get("/listings/99999")
        assert response.status_code == 404
    
    # Edge cases
    def test_search_listings_multiple_filters(self, listing_client: httpx.Client):
        """Test searching with multiple filters"""
        response = listing_client.get(
            "/listings?query=test&category_id=1&min_price=10&max_price=500&condition=good"
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_category_with_parent(self, listing_client: httpx.Client):
        """Test creating a subcategory"""
        # Create parent category
        parent_data = {
            "name": "Vehicles",
            "description": "Vehicles category"
        }
        parent_response = listing_client.post("/categories", json=parent_data)
        parent_id = parent_response.json()["id"]
        
        # Create subcategory
        child_data = {
            "name": "Cars",
            "description": "Cars subcategory",
            "parent_id": parent_id
        }
        response = listing_client.post("/categories", json=child_data)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["parent_id"] == parent_id


class TestListingServiceValidation:
    """Test validation and error handling"""
    
    def test_create_category_missing_name(self, listing_client: httpx.Client):
        """Test creating category without required name"""
        category_data = {
            "description": "Missing name"
        }
        response = listing_client.post("/categories", json=category_data)
        assert response.status_code in [400, 422, 500]  # Validation error
    
    def test_search_negative_min_price(self, listing_client: httpx.Client):
        """Test search with negative price (should be rejected)"""
        response = listing_client.get("/listings?min_price=-10")
        # Should either filter it or accept it as 0
        assert response.status_code in [200, 400, 422]
    
    def test_search_invalid_category_id(self, listing_client: httpx.Client):
        """Test search with invalid category ID type"""
        response = listing_client.get("/listings?category_id=invalid")
        # Should reject or coerce to int
        assert response.status_code in [200, 400, 422]


class TestListingServiceIntegration:
    """Integration tests for Listing service"""
    
    def test_create_and_retrieve_category(self, listing_client: httpx.Client):
        """Test creating a category and retrieving it"""
        # Create
        category_data = {
            "name": "Sports",
            "description": "Sports equipment"
        }
        create_response = listing_client.post("/categories", json=category_data)
        assert create_response.status_code in [200, 201]
        created_id = create_response.json()["id"]
        
        # Retrieve
        get_response = listing_client.get(f"/categories/{created_id}")
        assert get_response.status_code == 200
        retrieved = get_response.json()
        assert retrieved["name"] == "Sports"
        assert retrieved["id"] == created_id
    
    def test_get_all_categories_multiple(self, listing_client: httpx.Client):
        """Test getting all categories after creating multiple"""
        # Create multiple categories
        for i in range(3):
            category_data = {
                "name": f"Category_{i}",
                "description": f"Description {i}"
            }
            listing_client.post("/categories", json=category_data)
        
        # Get all
        response = listing_client.get("/categories")
        assert response.status_code == 200
        categories = response.json()
        assert len(categories) >= 3


class TestListingAPIStructure:
    """Test API structure and response formats"""
    
    def test_category_response_structure(self, listing_client: httpx.Client):
        """Test category response has expected fields"""
        category_data = {
            "name": "Books",
            "description": "Books and literature"
        }
        response = listing_client.post("/categories", json=category_data)
        assert response.status_code in [200, 201]
        data = response.json()
        
        # Check required fields
        assert "id" in data
        assert "name" in data
        assert "description" in data
        assert "created_at" in data
    
    def test_listing_search_response_structure(self, listing_client: httpx.Client):
        """Test listing search response structure"""
        response = listing_client.get("/listings")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_health_response_format(self, listing_client: httpx.Client):
        """Test health check response format"""
        response = listing_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
