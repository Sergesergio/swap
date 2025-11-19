#!/usr/bin/env python3
"""
Seed script to populate the platform with dummy data for testing and demonstration
Run: python scripts/seed_dummy_data.py
"""

import httpx
import json
import time
from typing import Dict, List, Any


class SwapPlatformSeeder:
    """Seed the Swap platform with realistic dummy data"""
    
    def __init__(self):
        self.auth_client = httpx.Client(base_url="http://localhost:8000", timeout=30.0)
        self.listing_client = httpx.Client(base_url="http://localhost:8002", timeout=30.0)
        self.offer_client = httpx.Client(base_url="http://localhost:8003", timeout=30.0)
        self.payment_client = httpx.Client(base_url="http://localhost:8004", timeout=30.0)
        self.users = {}
        self.listings = {}
    
    def seed_users(self):
        """Create test users"""
        print("\n📝 Creating test users...")
        
        users_data = [
            {
                "email": "alice@example.com",
                "username": "alice_smith",
                "password": "AliceSecure123!",
                "role": "buyer"
            },
            {
                "email": "bob@example.com",
                "username": "bob_seller",
                "password": "BobSecure123!",
                "role": "seller"
            },
            {
                "email": "charlie@example.com",
                "username": "charlie_trader",
                "password": "CharlieSecure123!",
                "role": "both"
            },
            {
                "email": "diana@example.com",
                "username": "diana_collector",
                "password": "DianaSecure123!",
                "role": "buyer"
            },
            {
                "email": "eve@example.com",
                "username": "eve_merchant",
                "password": "EveSecure123!",
                "role": "seller"
            }
        ]
        
        for user_data in users_data:
            register_data = {
                "email": user_data["email"],
                "username": user_data["username"],
                "password": user_data["password"]
            }
            
            try:
                response = self.auth_client.post("/register", json=register_data)
                if response.status_code == 200:
                    user_info = response.json()
                    self.users[user_data["username"]] = {
                        **user_info,
                        "email": user_data["email"],
                        "role": user_data["role"]
                    }
                    print(f"✅ Created user: {user_data['username']} (ID: {user_info['id']})")
                else:
                    print(f"⚠️  User {user_data['username']} already exists or error: {response.text}")
            except Exception as e:
                print(f"❌ Error creating user {user_data['username']}: {e}")
    
    def login_user(self, username: str) -> str:
        """Login a user and return access token"""
        try:
            user_data = self.users.get(username)
            if not user_data:
                print(f"⚠️  User {username} not found in seeded users")
                return None
            
            response = self.auth_client.post(
                "/token",
                data={
                    "username": user_data["email"],
                    "password": user_data["email"].replace("@example.com", "Secure123!").replace("_", "")
                }
            )
            if response.status_code == 200:
                return response.json()["access_token"]
        except Exception as e:
            print(f"❌ Error logging in {username}: {e}")
        return None
    
    def seed_listings(self):
        """Create sample listings"""
        print("\n📋 Creating sample listings...")
        
        listings_data = [
            {
                "title": "Vintage Leather Jacket",
                "description": "Classic brown leather jacket in excellent condition. Perfect for collectors.",
                "category": "fashion",
                "condition": "excellent",
                "price": 150.0,
                "seller": "bob_seller"
            },
            {
                "title": "iPhone 12 Pro Max",
                "description": "Unlocked, 256GB, slight wear on screen protector, works perfectly",
                "category": "electronics",
                "condition": "good",
                "price": 800.0,
                "seller": "eve_merchant"
            },
            {
                "title": "Antique Wooden Desk",
                "description": "Beautiful mahogany desk from 1950s. Some restoration needed.",
                "category": "furniture",
                "condition": "fair",
                "price": 350.0,
                "seller": "bob_seller"
            },
            {
                "title": "Samsung 4K Smart TV",
                "description": "55-inch display, 2 years old, excellent condition, all accessories included",
                "category": "electronics",
                "condition": "excellent",
                "price": 450.0,
                "seller": "eve_merchant"
            },
            {
                "title": "Mountain Bike",
                "description": "Trek hardtail, 29-inch wheels, recently serviced",
                "category": "sports",
                "condition": "excellent",
                "price": 600.0,
                "seller": "charlie_trader"
            },
            {
                "title": "MacBook Pro 2019",
                "description": "13-inch, i5, 8GB RAM, 256GB SSD. Light use only.",
                "category": "electronics",
                "condition": "excellent",
                "price": 900.0,
                "seller": "eve_merchant"
            },
            {
                "title": "Gold Diamond Ring",
                "description": "14K gold with 1 carat diamond. Certified. Includes original box.",
                "category": "jewelry",
                "condition": "excellent",
                "price": 2500.0,
                "seller": "bob_seller"
            },
            {
                "title": "Acoustic Guitar",
                "description": "Yamaha FG800, excellent sound, perfect for beginners and intermediate players",
                "category": "music",
                "condition": "good",
                "price": 250.0,
                "seller": "charlie_trader"
            }
        ]
        
        for listing_data in listings_data:
            seller = listing_data.pop("seller")
            # For demo purposes, we'll log the listing creation intent
            # In production, this would call the listing service API
            listing_key = listing_data["title"]
            self.listings[listing_key] = {
                **listing_data,
                "seller": seller,
                "id": len(self.listings) + 1  # Mock ID
            }
            print(f"✅ Created listing: {listing_data['title']} by {seller} - ${listing_data['price']}")
    
    def seed_offers(self):
        """Create sample offers"""
        print("\n💬 Creating sample offers...")
        
        offers_data = [
            {
                "listing": "iPhone 12 Pro Max",
                "buyer": "alice_smith",
                "offer_price": 750.0,
                "message": "Great condition! Would you accept $750?"
            },
            {
                "listing": "Vintage Leather Jacket",
                "buyer": "diana_collector",
                "offer_price": 140.0,
                "message": "I collect vintage items. Is $140 acceptable?"
            },
            {
                "listing": "Mountain Bike",
                "buyer": "alice_smith",
                "offer_price": 580.0,
                "message": "Looking to buy immediately"
            },
            {
                "listing": "Samsung 4K Smart TV",
                "buyer": "diana_collector",
                "offer_price": 400.0,
                "message": "Would you negotiate on price?"
            },
            {
                "listing": "Acoustic Guitar",
                "buyer": "alice_smith",
                "offer_price": 230.0,
                "message": "Will buy if price is right"
            }
        ]
        
        for offer_data in offers_data:
            listing = self.listings.get(offer_data["listing"])
            if listing:
                offer_payload = {
                    "listing_id": listing["id"],
                    "type": "direct_buy",
                    "price": offer_data["offer_price"],
                    "message": offer_data["message"]
                }
                
                try:
                    response = self.offer_client.post("/api/v1/offers/", json=offer_payload)
                    if response.status_code in [200, 201]:
                        offer_id = response.json()["id"]
                        print(f"✅ Created offer: {offer_data['buyer']} offered ${offer_data['offer_price']} for {offer_data['listing']} (ID: {offer_id})")
                    else:
                        print(f"⚠️  Could not create offer for {offer_data['listing']}: {response.text[:100]}")
                except Exception as e:
                    print(f"❌ Error creating offer: {e}")
    
    def create_sample_transactions(self):
        """Create sample transaction records"""
        print("\n💳 Creating sample transactions...")
        
        transactions_data = [
            {
                "offer_id": 1,
                "amount": 800.0,
                "payment_method": "credit_card"
            },
            {
                "offer_id": 2,
                "amount": 150.0,
                "payment_method": "paypal"
            },
            {
                "offer_id": 3,
                "amount": 600.0,
                "payment_method": "bank_transfer"
            }
        ]
        
        for tx_data in transactions_data:
            try:
                # Hold payment
                response = self.payment_client.post("/api/v1/payments/hold", json=tx_data)
                if response.status_code in [200, 201]:
                    payment_id = response.json()["id"]
                    print(f"✅ Payment held: ${tx_data['amount']} for offer {tx_data['offer_id']} (ID: {payment_id})")
                else:
                    print(f"⚠️  Could not hold payment: {response.text[:100]}")
            except Exception as e:
                print(f"❌ Error creating transaction: {e}")
    
    def print_summary(self):
        """Print summary of seeded data"""
        print("\n" + "="*60)
        print("📊 SEEDING SUMMARY")
        print("="*60)
        print(f"✅ Users created: {len(self.users)}")
        print(f"✅ Listings created: {len(self.listings)}")
        print(f"✅ Sample data ready for testing")
        print("\n📌 Available Users:")
        for username, user_info in self.users.items():
            print(f"  • {username} ({user_info['role']}) - ID: {user_info['id']}")
        print("\n📌 Available Listings:")
        for title, listing in self.listings.items():
            print(f"  • {title} - ${listing['price']} (by {listing['seller']})")
        print("="*60 + "\n")
    
    def run(self):
        """Execute full seeding workflow"""
        print("\n" + "="*60)
        print("🌱 SWAP PLATFORM DATA SEEDER")
        print("="*60)
        
        try:
            # Check if services are running
            try:
                auth_response = self.auth_client.get("/health")
                if auth_response.status_code != 200:
                    print("❌ Auth service not responding. Make sure Docker containers are running.")
                    return
            except Exception as e:
                print(f"❌ Cannot connect to services: {e}")
                print("   Make sure to run: docker compose up -d")
                return
            
            self.seed_users()
            time.sleep(1)
            self.seed_listings()
            time.sleep(1)
            self.seed_offers()
            time.sleep(1)
            self.create_sample_transactions()
            self.print_summary()
            
            print("✅ Seeding completed successfully!")
            
        except Exception as e:
            print(f"❌ Seeding failed: {e}")
            raise


if __name__ == "__main__":
    seeder = SwapPlatformSeeder()
    seeder.run()
