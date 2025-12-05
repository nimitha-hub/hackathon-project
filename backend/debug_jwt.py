#!/usr/bin/env python
"""Debug JWT token issue"""

from app import app, db, User
import json
import base64

with app.app_context():
    db.create_all()
    
    # Create test user
    user = User(email='test@test.com', password_hash='pass', name='Test')
    db.session.add(user)
    db.session.commit()
    print(f"Created user with ID: {user.id} (type: {type(user.id)})")
    
    # Use test client
    client = app.test_client()
    
    # Register
    resp = client.post('/api/auth/register', json={
        'email': 'newuser@test.com',
        'password': 'password123',
        'name': 'Test User'
    })
    print(f"\nRegistration response: {resp.status_code}")
    token = resp.get_json().get('access_token')
    print(f"Token: {token[:50]}...")
    
    # Decode token manually to see what's in it
    parts = token.split('.')
    payload = parts[1]
    # Add padding if needed
    padding = 4 - (len(payload) % 4)
    if padding != 4:
        payload += '=' * padding
    
    decoded = base64.urlsafe_b64decode(payload)
    print(f"Token payload: {decoded}")
    data = json.loads(decoded)
    print(f"Token data: {json.dumps(data, indent=2)}")
    print(f"Subject (sub) value: {data.get('sub')} (type: {type(data.get('sub'))})")
    
    # Now try to use the token
    print(f"\nTesting with token...")
    resp = client.get('/api/user/profile',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(f"Response status: {resp.status_code}")
    print(f"Response: {resp.get_json()}")
