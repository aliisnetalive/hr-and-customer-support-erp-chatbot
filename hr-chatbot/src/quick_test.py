#!/usr/bin/env python3
"""Quick API test for HR Chatbot"""
import requests
import json
import time

# Give server a moment to be ready
time.sleep(2)

print("\nTesting HR Chatbot API\n")

# Test 1: Health
print("1. Testing /health...")
try:
    r = requests.get("http://localhost:5001/health", timeout=5)
    health = r.json()
    print(f"   Status: {r.status_code}")
    print(f"   Ready: {health.get('chatbot_ready')}")
    print(json.dumps(health, indent=2))
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*60)

# Test 2: Ask question
print("\n2. Testing /ask endpoint...")
try:
    r = requests.post(
        "http://localhost:5001/ask",
        json={"question": "What is the policy on sick leave?"},
        timeout=30
    )
    print(f"   Status: {r.status_code}")
    data = r.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"   Error: {e}")

print("\nTest complete!")
