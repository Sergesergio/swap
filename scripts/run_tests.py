#!/usr/bin/env python3
"""
Test runner script for all tests
Runs: unit tests, integration tests, and end-to-end tests
"""

import subprocess
import sys
import os

def run_tests():
    """Run all test suites"""
    print("\n" + "="*70)
    print("🧪 SWAP PLATFORM TEST SUITE RUNNER")
    print("="*70)
    
    test_suites = [
        {
            "name": "Auth Service Unit Tests",
            "file": "tests/test_auth_unit.py",
            "description": "Register, login, token refresh, current user"
        },
        {
            "name": "Offer & Payment Services Unit Tests",
            "file": "tests/test_offer_payment_unit.py",
            "description": "Offer creation, payment holds, payment releases"
        },
        {
            "name": "Integration Tests",
            "file": "tests/test_integration.py",
            "description": "Offer and payment service integration"
        },
        {
            "name": "End-to-End Tests",
            "file": "tests/test_e2e.py",
            "description": "Complete user workflows"
        }
    ]
    
    results = []
    
    for suite in test_suites:
        print(f"\n{'─'*70}")
        print(f"📋 {suite['name']}")
        print(f"   {suite['description']}")
        print(f"{'─'*70}")
        
        cmd = [
            sys.executable,
            "-m", "pytest",
            suite["file"],
            "-v",
            "--tb=short",
            "--co lor=yes",
            "-x"  # Stop on first failure for quicker feedback
        ]
        
        result = subprocess.run(cmd, cwd="/app" if os.path.exists("/app") else ".")
        results.append({
            "name": suite["name"],
            "status": "✅ PASSED" if result.returncode == 0 else "❌ FAILED",
            "code": result.returncode
        })
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results if r["code"] == 0)
    total = len(results)
    
    for result in results:
        print(f"{result['status']} - {result['name']}")
    
    print(f"\nTotal: {passed}/{total} suites passed")
    print("="*70 + "\n")
    
    return all(r["code"] == 0 for r in results)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
