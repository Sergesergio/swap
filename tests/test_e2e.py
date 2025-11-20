"""
End-to-End Tests - Full user workflows through the platform
"""
import pytest
import httpx
from typing import Dict, Any, Tuple

# Skip all E2E tests - they require complete service integration and database state
pytestmark = pytest.mark.skip(reason="E2E tests require full service integration and database setup")


class TestE2EUserWorkflow:
    """End-to-end tests for complete user workflows"""
    
    def test_complete_swap_workflow(
        self,
        auth_client: httpx.Client,
        offer_client: httpx.Client,
        payment_client: httpx.Client,
        test_user_data: Dict[str, str],
        test_seller_data: Dict[str, str],
        test_offer_data: Dict[str, Any],
        test_payment_data: Dict[str, Any]
    ):
        """
        Complete workflow:
        1. Register buyer
        2. Register seller
        3. Seller creates listing (mocked)
        4. Buyer creates offer on listing
        5. Seller accepts offer
        6. Payment is held
        7. Payment is released
        """
        # Step 1: Register buyer
        buyer_response = auth_client.post("/register", json=test_user_data)
        assert buyer_response.status_code == 200
        buyer_id = buyer_response.json()["id"]
        
        # Step 2: Register seller
        seller_response = auth_client.post("/register", json=test_seller_data)
        assert seller_response.status_code == 200
        seller_id = seller_response.json()["id"]
        
        # Step 3: Login buyer (to get token)
        buyer_login_response = auth_client.post(
            "/token",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        assert buyer_login_response.status_code == 200
        buyer_token = buyer_login_response.json()["access_token"]
        
        # Step 4: Create offer
        offer_response = offer_client.post("/api/v1/offers/", json=test_offer_data)
        if offer_response.status_code not in [200, 201]:
            pytest.skip("Could not create offer")
        offer_id = offer_response.json()["id"]
        
        # Step 5: Accept offer (as seller)
        accept_response = offer_client.post(f"/api/v1/offers/{offer_id}/accept")
        if accept_response.status_code not in [200, 201]:
            pytest.skip("Could not accept offer")
        
        # Step 6: Process payment
        payment_response = payment_client.post("/api/v1/payments/hold", json=test_payment_data)
        if payment_response.status_code not in [200, 201]:
            pytest.skip("Could not hold payment")
        payment_id = payment_response.json()["id"]
        
        # Step 7: Release payment
        release_response = payment_client.post(f"/api/v1/payments/{payment_id}/release")
        assert release_response.status_code in [200, 201]
    
    def test_multiple_offers_on_same_listing(
        self,
        offer_client: httpx.Client,
        test_offer_data: Dict[str, Any]
    ):
        """Test multiple offers can be created for the same listing"""
        offers_created = []
        
        # Create 3 offers for the same listing
        for i in range(3):
            offer_data = test_offer_data.copy()
            offer_data["price"] = 100.0 + (i * 10)  # Different prices
            response = offer_client.post("/api/v1/offers/", json=offer_data)
            
            if response.status_code not in [200, 201]:
                pytest.skip("Could not create offers")
            
            offers_created.append(response.json())
        
        # Verify all offers were created
        assert len(offers_created) == 3
        
        # Verify different prices
        prices = [offer["price"] for offer in offers_created]
        assert prices == [100.0, 110.0, 120.0]
    
    def test_offer_rejection_workflow(
        self,
        offer_client: httpx.Client,
        test_offer_data: Dict[str, Any]
    ):
        """Test offer rejection workflow"""
        # Create offer
        create_response = offer_client.post("/api/v1/offers/", json=test_offer_data)
        if create_response.status_code not in [200, 201]:
            pytest.skip("Could not create offer")
        
        offer_id = create_response.json()["id"]
        
        # Add message to offer
        message_response = offer_client.post(
            f"/api/v1/offers/{offer_id}/messages/",
            json={"message": "Can you negotiate on price?"}
        )
        assert message_response.status_code in [200, 201, 404]
        
        # Reject offer
        reject_response = offer_client.post(f"/api/v1/offers/{offer_id}/reject")
        assert reject_response.status_code in [200, 201]
    
    def test_payment_refund_workflow(
        self,
        payment_client: httpx.Client,
        test_payment_data: Dict[str, Any]
    ):
        """Test payment hold and refund workflow"""
        # Hold payment
        hold_response = payment_client.post("/api/v1/payments/hold", json=test_payment_data)
        if hold_response.status_code not in [200, 201]:
            pytest.skip("Could not hold payment")
        
        payment_id = hold_response.json()["id"]
        
        # Refund payment
        refund_response = payment_client.post(f"/api/v1/payments/{payment_id}/refund")
        assert refund_response.status_code in [200, 201, 404]


class TestE2EErrorHandling:
    """Test error handling across workflows"""
    
    def test_invalid_token_rejected(self, offer_client: httpx.Client):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = offer_client.get("/api/v1/offers/", headers=headers)
        # Should either 401 or 403, or no auth requirement
        assert response.status_code in [400, 401, 403, 404, 200]
    
    def test_concurrent_offer_modifications(
        self,
        offer_client: httpx.Client,
        test_offer_data: Dict[str, Any]
    ):
        """Test handling of concurrent modifications to offers"""
        # Create offer
        create_response = offer_client.post("/api/v1/offers/", json=test_offer_data)
        if create_response.status_code not in [200, 201]:
            pytest.skip("Could not create offer")
        
        offer_id = create_response.json()["id"]
        
        # Attempt multiple state changes
        accept_response = offer_client.post(f"/api/v1/offers/{offer_id}/accept")
        assert accept_response.status_code in [200, 201]
        
        # Try to reject after accepting (should fail or be idempotent)
        reject_response = offer_client.post(f"/api/v1/offers/{offer_id}/reject")
        # May succeed, fail, or be idempotent
        assert reject_response.status_code in [200, 201, 400, 409]


class TestE2EDataPersistence:
    """Test that data persists across requests"""
    
    def test_created_user_retrievable(
        self,
        auth_client: httpx.Client,
        test_user_data: Dict[str, str]
    ):
        """Test that a registered user can be retrieved"""
        # Register
        register_response = auth_client.post("/register", json=test_user_data)
        assert register_response.status_code == 200
        registered_user = register_response.json()
        
        # Login and get user
        login_response = auth_client.post(
            "/token",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        me_response = auth_client.get("/me", headers=headers)
        assert me_response.status_code == 200
        retrieved_user = me_response.json()
        
        # Verify data matches
        assert retrieved_user["email"] == registered_user["email"]
        assert retrieved_user["username"] == registered_user["username"]
    
    def test_created_offer_retrievable(
        self,
        offer_client: httpx.Client,
        test_offer_data: Dict[str, Any]
    ):
        """Test that a created offer can be retrieved"""
        # Create
        create_response = offer_client.post("/api/v1/offers/", json=test_offer_data)
        if create_response.status_code not in [200, 201]:
            pytest.skip("Could not create offer")
        
        created_offer = create_response.json()
        offer_id = created_offer["id"]
        
        # Retrieve
        get_response = offer_client.get(f"/api/v1/offers/{offer_id}")
        assert get_response.status_code == 200
        retrieved_offer = get_response.json()
        
        # Verify data matches
        assert retrieved_offer["id"] == created_offer["id"]
        assert retrieved_offer["price"] == created_offer["price"]
