#!/bin/bash

# Swap Platform Frontend-Backend Integration Tests
# Tests API endpoints through Nginx gateway

set -e

API_BASE="http://localhost:8080"
FRONTEND_URL="http://localhost:3000"

echo "🧪 Starting Swap Platform Integration Tests"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local expected_status=$4
    
    echo -n "Testing: $name ... "
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$API_BASE$endpoint" 2>/dev/null || echo "error\nFailed")
    elif [ "$method" == "HEAD" ]; then
        response=$(curl -s -I -w "%{http_code}" -X HEAD "$API_BASE$endpoint" 2>/dev/null | tail -1 || echo "Failed")
    fi
    
    status_code=$(echo "$response" | tail -1)
    
    if [ "$status_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        ((FAILED++))
    fi
}

# Service health checks
echo -e "${YELLOW}1. Service Health Checks${NC}"
test_endpoint "Nginx Gateway Health" "GET" "/health" "200"
test_endpoint "Auth Service Health" "GET" "/api/auth/health" "200"
test_endpoint "User Service Health" "GET" "/api/users/health" "200"
test_endpoint "Listing Service Health" "GET" "/api/listings/health" "200"
test_endpoint "Offer Service Health" "GET" "/api/offers/health" "200"
test_endpoint "Payment Service Health" "GET" "/api/payments/health" "200"
test_endpoint "Chat Service Health" "GET" "/api/chat/health" "200"
test_endpoint "Notification Service Health" "GET" "/api/notifications/health" "200"

echo ""
echo -e "${YELLOW}2. Frontend Access${NC}"
echo -n "Testing: Frontend Home Page ... "
frontend_status=$(curl -s -w "%{http_code}" -o /dev/null "$FRONTEND_URL/")
if [ "$frontend_status" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Status: $frontend_status)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} (Expected: 200, Got: $frontend_status)"
    ((FAILED++))
fi

echo ""
echo -e "${YELLOW}3. API Authentication Endpoints${NC}"
test_endpoint "Auth Register Docs" "GET" "/api/auth/docs" "200"
test_endpoint "Auth OpenAPI Schema" "GET" "/api/auth/openapi.json" "200"

echo ""
echo -e "${YELLOW}4. API Service Endpoints${NC}"
test_endpoint "User Service Docs" "GET" "/api/users/docs" "200"
test_endpoint "Listing Service Docs" "GET" "/api/listings/docs" "200"
test_endpoint "Offer Service Docs" "GET" "/api/offers/docs" "200"
test_endpoint "Payment Service Docs" "GET" "/api/payments/docs" "200"
test_endpoint "Chat Service Docs" "GET" "/api/chat/docs" "200"

echo ""
echo "=========================================="
echo -e "Results: ${GREEN}$PASSED Passed${NC} | ${RED}$FAILED Failed${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
