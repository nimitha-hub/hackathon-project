#!/usr/bin/env python
"""Test if app module can be imported"""
import sys
import traceback

try:
    from app import app, db, User
    print("SUCCESS: App module imported successfully")
    print(f"App: {app}")
    print(f"Flask routes registered: {len(app.url_map._rules)}")
    
    # Try a test request
    with app.test_client() as client:
        print("\nTesting /api/auth/login endpoint...")
        response = client.post('/api/auth/login', 
                              json={"email": "test@example.com", "password": "test"},
                              content_type='application/json')
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.get_json()}")
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
