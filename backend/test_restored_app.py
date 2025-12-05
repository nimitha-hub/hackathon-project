#!/usr/bin/env python
"""Test the restored app with test client"""

from app import app, db, User
import json

print("Testing restored HealMate app...")

with app.app_context():
    db.create_all()
    
    client = app.test_client()
    
    # Test registration
    print("\n1. Testing registration...")
    resp = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    print(f"   Status: {resp.status_code}")
    data = resp.get_json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    
    if resp.status_code == 201:
        token = data.get('access_token')
        user_id = data.get('user_id')
        
        # Test get profile
        print(f"\n2. Testing get profile...")
        resp = client.get('/api/user/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {json.dumps(resp.get_json(), indent=2)}")
        
        # Test update profile
        print(f"\n3. Testing update profile...")
        resp = client.put('/api/user/profile', json={
            'nickname': 'TestNick',
            'height_cm': 170,
            'weight_kg': 75,
            'blood_type': 'O+',
            'sleep_goal_hours': 8
        }, headers={'Authorization': f'Bearer {token}'})
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {json.dumps(resp.get_json(), indent=2)}")
        
        # Verify profile was updated
        print(f"\n4. Verifying profile update...")
        resp = client.get('/api/user/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        data = resp.get_json()
        print(f"   Nickname: {data.get('nickname')}")
        print(f"   Height: {data.get('height_cm')}")
        
print("\nAll tests completed!")
