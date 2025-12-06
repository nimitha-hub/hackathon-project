import os
import sqlite3

# Delete old databases
db_files = [
    'backend/instance/healmate.db',
    'backend/instance/health_assistant.db'
]

for db_file in db_files:
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"Deleted {db_file}")
        except:
            print(f"Could not delete {db_file}")

# Create fresh database with correct schema
os.makedirs('backend/instance', exist_ok=True)
conn = sqlite3.connect('backend/instance/health_assistant.db')
cursor = conn.cursor()

# Drop existing tables
cursor.execute('DROP TABLE IF EXISTS medications')
cursor.execute('DROP TABLE IF EXISTS chat_history')
cursor.execute('DROP TABLE IF EXISTS users')

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    nickname TEXT,
    age INTEGER,
    height_cm REAL,
    weight_kg REAL,
    blood_type TEXT,
    blood_sugar_fasting REAL,
    blood_pressure_sys INTEGER,
    blood_pressure_dia INTEGER,
    job_title TEXT,
    job_stress_level INTEGER,
    sleep_goal_hours INTEGER DEFAULT 8,
    exercise_goal_minutes INTEGER DEFAULT 30,
    hobbies TEXT,
    likes TEXT,
    dislikes TEXT,
    meditation_preference TEXT,
    video_reminder_interval INTEGER DEFAULT 3,
    has_menstrual_cycle INTEGER DEFAULT 0,
    menstrual_cycle_day INTEGER,
    dietary_restrictions TEXT,
    allergies TEXT,
    chronic_conditions TEXT,
    work_start_time TEXT,
    work_end_time TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create medications table
cursor.execute('''
CREATE TABLE medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    dosage TEXT,
    frequency TEXT,
    scheduled_times TEXT,
    reason TEXT,
    stock_quantity INTEGER DEFAULT 0,
    refill_threshold INTEGER DEFAULT 5,
    last_taken TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Create chat_history table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_user INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()
conn.close()

print("\n✅ Database created successfully with correct schema!")
print("\nNext steps:")
print("1. Start backend: cd backend && python app.py")
print("2. Start frontend: cd frontend && npm start")
print("3. Go to http://localhost:3000")
print("4. Register a new account and complete profile setup")
