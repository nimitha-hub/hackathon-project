#!/usr/bin/env python
"""Test chat endpoint"""

from app import app
import json

with app.app_context():
    client = app.test_client()
    
    # First login to get token
    print("1. Logging in...")
    resp = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.get_json()}")
        print("\nTrying to register first...")
        resp = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        })
        if resp.status_code != 201:
            print(f"Register failed: {resp.get_json()}")
            exit(1)
    
    token = resp.get_json().get('access_token')
    print(f"✓ Got token")
    
    # Test chat with different questions
    test_messages = [
        "hello",
        "I need a sleep schedule",
        "Create a diet plan for me",
        "Give me a workout routine"
    ]
    
    for msg in test_messages:
        print(f"\n2. Testing chat: '{msg}'")
        resp = client.post('/api/chat', 
            json={'message': msg},
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        data = resp.get_json()
        response = data.get('assistant_response', '')
        print(f"   Response preview: {response[:200]}...")
        print(f"   Full length: {len(response)} characters")

print("\n✓ All chat tests completed!")
