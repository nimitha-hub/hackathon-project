import sqlite3
import sys

try:
    conn = sqlite3.connect('instance/health_assistant.db')
    cursor = conn.cursor()
    
    # Check users
    cursor.execute('SELECT email, name FROM users')
    users = cursor.fetchall()
    print(f'Total users: {len(users)}')
    for user in users:
        print(f'  Email: {user[0]}, Name: {user[1]}')
    
    # Check medications
    cursor.execute('SELECT COUNT(*) FROM medications')
    med_count = cursor.fetchone()[0]
    print(f'\nTotal medications: {med_count}')
    
    conn.close()
    print('\nDatabase check complete!')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
