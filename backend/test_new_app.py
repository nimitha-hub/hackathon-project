#!/usr/bin/env python
"""Test the new minimal app"""

from app_new import app, db, User, Medication

print("Testing new minimal Flask app...")

with app.app_context():
    # Initialize database
    db.create_all()
    
    # Test client
    client = app.test_client()
    
    print("\n1. Testing health endpoint...")
    resp = client.get('/api/health')
    print(f"   Status: {resp.status_code}")
    print(f"   Body: {resp.get_json()}")
    
    print("\n2. Testing registration...")
    resp = client.post('/api/auth/register', json={
        'email': 'newuser@test.com',
        'password': 'password123',
        'name': 'Test User'
    })
    print(f"   Status: {resp.status_code}")
    print(f"   Body: {resp.get_json()}")
    
    if resp.status_code == 201:
        token = resp.get_json().get('access_token')
        user_id = resp.get_json().get('user_id')
        
        print(f"\n3. Testing profile update with token...")
        resp = client.put('/api/user/profile', 
            json={
                'nickname': 'Test Nick',
                'height_cm': 170,
                'weight_kg': 75,
                'blood_type': 'O+',
                'sleep_goal_hours': 8
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        print(f"   Body: {resp.get_json()}")
        
        print(f"\n4. Testing add medication...")
        resp = client.post('/api/medications',
            json={
                'name': 'Aspirin',
                'dosage': '100mg',
                'frequency': 'Daily',
                'stock_quantity': 30
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        print(f"   Body: {resp.get_json()}")
        
        print(f"\n5. Testing get profile...")
        resp = client.get('/api/user/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        data = resp.get_json()
        print(f"   Profile data: email={data.get('email')}, nickname={data.get('nickname')}")
        print(f"   Medications count: {len(data.get('medications', []))}")
        
        print(f"\n6. Testing chat...")
        resp = client.post('/api/chat',
            json={'message': 'Tell me about medication'},
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"   Status: {resp.status_code}")
        print(f"   Body: {resp.get_json()}")

print("\n✓ All tests completed!")
