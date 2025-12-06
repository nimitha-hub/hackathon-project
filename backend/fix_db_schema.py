import sqlite3

conn = sqlite3.connect('instance/health_assistant.db')
cursor = conn.cursor()

try:
    # Add missing columns to users table
    columns_to_add = [
        ('age', 'INTEGER'),
        ('job_title', 'TEXT'),
        ('job_stress_level', 'INTEGER'),
        ('exercise_goal_minutes', 'INTEGER'),
        ('hobbies', 'TEXT'),
        ('likes', 'TEXT'),
        ('dislikes', 'TEXT'),
        ('meditation_preference', 'TEXT'),
        ('video_reminder_interval', 'INTEGER'),
        ('has_menstrual_cycle', 'INTEGER'),
        ('menstrual_cycle_day', 'INTEGER'),
        ('dietary_restrictions', 'TEXT'),
        ('allergies', 'TEXT'),
        ('chronic_conditions', 'TEXT'),
        ('work_start_time', 'TEXT'),
        ('work_end_time', 'TEXT')
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}')
            print(f'Added column: {col_name}')
        except Exception as e:
            if 'duplicate column name' in str(e).lower():
                print(f'Column {col_name} already exists')
            else:
                print(f'Error adding {col_name}: {e}')
    
    # Add missing columns to medications table
    med_columns = [
        ('scheduled_times', 'TEXT'),
        ('reason', 'TEXT'),
        ('refill_threshold', 'INTEGER'),
        ('last_taken', 'TEXT')
    ]
    
    for col_name, col_type in med_columns:
        try:
            cursor.execute(f'ALTER TABLE medications ADD COLUMN {col_name} {col_type}')
            print(f'Added medication column: {col_name}')
        except Exception as e:
            if 'duplicate column name' in str(e).lower():
                print(f'Column {col_name} already exists')
            else:
                print(f'Error adding {col_name}: {e}')
    
    conn.commit()
    print('\nDatabase schema updated successfully!')
    
    # Verify
    cursor.execute('PRAGMA table_info(users)')
    cols = [row[1] for row in cursor.fetchall()]
    print(f'\nTotal user columns: {len(cols)}')
    
except Exception as e:
    print(f'ERROR: {e}')
finally:
    conn.close()
