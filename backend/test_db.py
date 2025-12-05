#!/usr/bin/env python
from app import db, app, User
import sys

with app.app_context():
    try:
        users = User.query.all()
        print(f"SUCCESS: Connected to database. Found {len(users)} users")
        for user in users:
            print(f"  - {user.email} (ID: {user.id}, nickname: {user.nickname})")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
