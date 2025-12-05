from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    
    # Personal Information
    age = db.Column(db.Integer)
    height_cm = db.Column(db.Float)  # in cm
    weight_kg = db.Column(db.Float)  # in kg
    blood_type = db.Column(db.String(10))
    
    # Health Parameters
    blood_sugar_fasting = db.Column(db.Float)  # mg/dL
    blood_pressure_sys = db.Column(db.Integer)  # systolic
    blood_pressure_dia = db.Column(db.Integer)  # diastolic
    
    # Lifestyle
    job_title = db.Column(db.String(120))
    job_stress_level = db.Column(db.String(20))  # low, medium, high
    sleep_goal_hours = db.Column(db.Float, default=8)
    exercise_goal_minutes = db.Column(db.Integer, default=30)
    
    # Preferences
    hobbies = db.Column(db.Text)  # JSON string
    likes = db.Column(db.Text)
    dislikes = db.Column(db.Text)
    meditation_preference = db.Column(db.String(50))  # morning, evening, both
    video_reminder_interval = db.Column(db.Integer, default=3)  # days
    
    # Health Conditions
    has_menstrual_cycle = db.Column(db.Boolean, default=False)
    menstrual_cycle_day = db.Column(db.Integer)  # 1-28
    dietary_restrictions = db.Column(db.Text)
    allergies = db.Column(db.Text)
    chronic_conditions = db.Column(db.Text)
    
    # Account Info
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medications = db.relationship('Medication', backref='user', lazy=True, cascade='all, delete-orphan')
    health_checks = db.relationship('HealthCheckIn', backref='user', lazy=True, cascade='all, delete-orphan')
    daily_goals = db.relationship('DailyGoal', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True, cascade='all, delete-orphan')


class Medication(db.Model):
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(50))  # e.g., "500mg"
    frequency = db.Column(db.String(50), nullable=False)  # e.g., "twice daily", "once daily"
    scheduled_times = db.Column(db.Text)  # JSON array of times ["08:00", "20:00"]
    reason = db.Column(db.String(200))
    
    # Stock Tracking
    stock_quantity = db.Column(db.Integer, nullable=False)  # pills/tablets remaining
    refill_threshold = db.Column(db.Integer, default=10)  # remind when below this
    
    # Tracking
    last_taken = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    intake_logs = db.relationship('MedicationIntake', backref='medication', lazy=True, cascade='all, delete-orphan')


class MedicationIntake(db.Model):
    __tablename__ = 'medication_intakes'
    
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)
    skipped = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class HealthCheckIn(db.Model):
    __tablename__ = 'health_checkins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    check_in_date = db.Column(db.Date, default=lambda: datetime.utcnow().date())
    
    # Daily Health Data
    mood = db.Column(db.String(50))  # happy, neutral, sad, anxious, etc.
    stress_level = db.Column(db.Integer)  # 1-10
    sleep_hours = db.Column(db.Float)
    water_intake_liters = db.Column(db.Float, default=0)
    meals_logged = db.Column(db.Integer, default=0)  # count of meals logged
    exercise_minutes = db.Column(db.Integer, default=0)
    meditation_minutes = db.Column(db.Integer, default=0)
    screen_breaks = db.Column(db.Integer, default=0)
    
    # Menstrual Cycle Tracking
    menstrual_flow = db.Column(db.String(20))  # light, medium, heavy
    menstrual_cramps = db.Column(db.Boolean, default=False)
    
    # Measurements
    blood_sugar = db.Column(db.Float)
    blood_pressure_sys = db.Column(db.Integer)
    blood_pressure_dia = db.Column(db.Integer)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailyGoal(db.Model):
    __tablename__ = 'daily_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    goal_date = db.Column(db.Date, default=lambda: datetime.utcnow().date())
    goal_type = db.Column(db.String(50), nullable=False)  # water, exercise, meditation, sleep, meals, medication
    target_value = db.Column(db.Float)  # e.g., 8 liters, 30 minutes
    current_value = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20))  # liters, minutes, hours, pills
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    role = db.Column(db.String(20), nullable=False)  # "user" or "assistant"
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WeeklyHealthReport(db.Model):
    __tablename__ = 'weekly_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    week_start_date = db.Column(db.Date)
    week_end_date = db.Column(db.Date)
    
    # Metrics
    total_sleep_hours = db.Column(db.Float)
    total_water_liters = db.Column(db.Float)
    medication_adherence_percent = db.Column(db.Float)
    exercise_minutes = db.Column(db.Integer)
    meditation_minutes = db.Column(db.Integer)
    goals_completed = db.Column(db.Integer)
    goals_missed = db.Column(db.Integer)
    average_mood = db.Column(db.String(50))
    
    report_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== API ROUTES ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()}), 200


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=data['email'],
            password_hash=data['password'],  # In production, hash this!
            name=data['name']
        )
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user_id': user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or user.password_hash != data.get('password'):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user_id': user.id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'age': user.age,
            'height_cm': user.height_cm,
            'weight_kg': user.weight_kg,
            'blood_type': user.blood_type,
            'blood_sugar_fasting': user.blood_sugar_fasting,
            'blood_pressure': f"{user.blood_pressure_sys}/{user.blood_pressure_dia}",
            'job_title': user.job_title,
            'job_stress_level': user.job_stress_level,
            'sleep_goal_hours': user.sleep_goal_hours,
            'exercise_goal_minutes': user.exercise_goal_minutes,
            'hobbies': user.hobbies,
            'likes': user.likes,
            'dislikes': user.dislikes,
            'has_menstrual_cycle': user.has_menstrual_cycle,
            'dietary_restrictions': user.dietary_restrictions,
            'allergies': user.allergies,
            'chronic_conditions': user.chronic_conditions,
            'meditation_preference': user.meditation_preference,
            'video_reminder_interval': user.video_reminder_interval,
            'created_at': user.created_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update all provided fields
        if 'age' in data:
            user.age = data['age']
        if 'height_cm' in data:
            user.height_cm = data['height_cm']
        if 'weight_kg' in data:
            user.weight_kg = data['weight_kg']
        if 'blood_type' in data:
            user.blood_type = data['blood_type']
        if 'blood_sugar_fasting' in data:
            user.blood_sugar_fasting = data['blood_sugar_fasting']
        if 'blood_pressure_sys' in data:
            user.blood_pressure_sys = data['blood_pressure_sys']
        if 'blood_pressure_dia' in data:
            user.blood_pressure_dia = data['blood_pressure_dia']
        if 'job_title' in data:
            user.job_title = data['job_title']
        if 'job_stress_level' in data:
            user.job_stress_level = data['job_stress_level']
        if 'sleep_goal_hours' in data:
            user.sleep_goal_hours = data['sleep_goal_hours']
        if 'exercise_goal_minutes' in data:
            user.exercise_goal_minutes = data['exercise_goal_minutes']
        if 'hobbies' in data:
            user.hobbies = data['hobbies']
        if 'likes' in data:
            user.likes = data['likes']
        if 'dislikes' in data:
            user.dislikes = data['dislikes']
        if 'has_menstrual_cycle' in data:
            user.has_menstrual_cycle = data['has_menstrual_cycle']
        if 'menstrual_cycle_day' in data:
            user.menstrual_cycle_day = data['menstrual_cycle_day']
        if 'dietary_restrictions' in data:
            user.dietary_restrictions = data['dietary_restrictions']
        if 'allergies' in data:
            user.allergies = data['allergies']
        if 'chronic_conditions' in data:
            user.chronic_conditions = data['chronic_conditions']
        if 'meditation_preference' in data:
            user.meditation_preference = data['meditation_preference']
        if 'video_reminder_interval' in data:
            user.video_reminder_interval = data['video_reminder_interval']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Medication Management Routes

@app.route('/api/medications', methods=['GET'])
@jwt_required()
def get_medications():
    """Get all medications for user"""
    try:
        user_id = get_jwt_identity()
        medications = Medication.query.filter_by(user_id=user_id).all()
        
        meds_list = [{
            'id': med.id,
            'name': med.name,
            'dosage': med.dosage,
            'frequency': med.frequency,
            'scheduled_times': med.scheduled_times,
            'stock_quantity': med.stock_quantity,
            'refill_threshold': med.refill_threshold,
            'reason': med.reason,
            'last_taken': med.last_taken.isoformat() if med.last_taken else None
        } for med in medications]
        
        return jsonify(meds_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/medications', methods=['POST'])
@jwt_required()
def add_medication():
    """Add a new medication"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('name') or not data.get('frequency'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        medication = Medication(
            user_id=user_id,
            name=data['name'],
            dosage=data.get('dosage'),
            frequency=data['frequency'],
            scheduled_times=data.get('scheduled_times'),  # JSON array string
            reason=data.get('reason'),
            stock_quantity=data.get('stock_quantity', 0),
            refill_threshold=data.get('refill_threshold', 10)
        )
        
        db.session.add(medication)
        db.session.commit()
        
        return jsonify({'message': 'Medication added', 'id': medication.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/medications/<int:med_id>', methods=['PUT'])
@jwt_required()
def update_medication(med_id):
    """Update medication"""
    try:
        user_id = get_jwt_identity()
        medication = Medication.query.filter_by(id=med_id, user_id=user_id).first()
        
        if not medication:
            return jsonify({'error': 'Medication not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            medication.name = data['name']
        if 'dosage' in data:
            medication.dosage = data['dosage']
        if 'frequency' in data:
            medication.frequency = data['frequency']
        if 'scheduled_times' in data:
            medication.scheduled_times = data['scheduled_times']
        if 'stock_quantity' in data:
            medication.stock_quantity = data['stock_quantity']
        if 'refill_threshold' in data:
            medication.refill_threshold = data['refill_threshold']
        
        db.session.commit()
        return jsonify({'message': 'Medication updated'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/medications/<int:med_id>/intake', methods=['POST'])
@jwt_required()
def log_medication_intake(med_id):
    """Log medication intake"""
    try:
        user_id = get_jwt_identity()
        medication = Medication.query.filter_by(id=med_id, user_id=user_id).first()
        
        if not medication:
            return jsonify({'error': 'Medication not found'}), 404
        
        data = request.get_json()
        
        intake = MedicationIntake(
            medication_id=med_id,
            skipped=data.get('skipped', False),
            notes=data.get('notes')
        )
        
        if not data.get('skipped', False):
            medication.stock_quantity -= 1
            medication.last_taken = datetime.utcnow()
        
        db.session.add(intake)
        db.session.commit()
        
        return jsonify({'message': 'Medication intake logged'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Health Check-In Routes

@app.route('/api/health-checkin', methods=['POST'])
@jwt_required()
def create_health_checkin():
    """Create daily health check-in"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if already checked in today
        today = datetime.utcnow().date()
        existing = HealthCheckIn.query.filter_by(user_id=user_id, check_in_date=today).first()
        
        if existing:
            return jsonify({'error': 'Already checked in today'}), 400
        
        checkin = HealthCheckIn(
            user_id=user_id,
            check_in_date=today,
            mood=data.get('mood'),
            stress_level=data.get('stress_level'),
            sleep_hours=data.get('sleep_hours'),
            water_intake_liters=data.get('water_intake_liters', 0),
            meals_logged=data.get('meals_logged', 0),
            exercise_minutes=data.get('exercise_minutes', 0),
            meditation_minutes=data.get('meditation_minutes', 0),
            menstrual_flow=data.get('menstrual_flow'),
            menstrual_cramps=data.get('menstrual_cramps', False),
            blood_sugar=data.get('blood_sugar'),
            blood_pressure_sys=data.get('blood_pressure_sys'),
            blood_pressure_dia=data.get('blood_pressure_dia'),
            notes=data.get('notes')
        )
        
        db.session.add(checkin)
        db.session.commit()
        
        return jsonify({'message': 'Health check-in created', 'id': checkin.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/health-checkin/today', methods=['GET'])
@jwt_required()
def get_today_checkin():
    """Get today's health check-in"""
    try:
        user_id = get_jwt_identity()
        today = datetime.utcnow().date()
        
        checkin = HealthCheckIn.query.filter_by(user_id=user_id, check_in_date=today).first()
        
        if not checkin:
            return jsonify({'error': 'No check-in found for today'}), 404
        
        return jsonify({
            'id': checkin.id,
            'mood': checkin.mood,
            'stress_level': checkin.stress_level,
            'sleep_hours': checkin.sleep_hours,
            'water_intake_liters': checkin.water_intake_liters,
            'exercise_minutes': checkin.exercise_minutes,
            'meditation_minutes': checkin.meditation_minutes,
            'notes': checkin.notes
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health-checkin/<int:checkin_id>', methods=['PUT'])
@jwt_required()
def update_health_checkin(checkin_id):
    """Update health check-in"""
    try:
        user_id = get_jwt_identity()
        checkin = HealthCheckIn.query.filter_by(id=checkin_id, user_id=user_id).first()
        
        if not checkin:
            return jsonify({'error': 'Check-in not found'}), 404
        
        data = request.get_json()
        
        if 'mood' in data:
            checkin.mood = data['mood']
        if 'stress_level' in data:
            checkin.stress_level = data['stress_level']
        if 'sleep_hours' in data:
            checkin.sleep_hours = data['sleep_hours']
        if 'water_intake_liters' in data:
            checkin.water_intake_liters = data['water_intake_liters']
        if 'exercise_minutes' in data:
            checkin.exercise_minutes = data['exercise_minutes']
        if 'meditation_minutes' in data:
            checkin.meditation_minutes = data['meditation_minutes']
        if 'notes' in data:
            checkin.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({'message': 'Check-in updated'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== CHATBOT ROUTES ====================

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat_with_assistant():
    """Chat with AI assistant"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Save user message
        user_msg = ChatMessage(user_id=user_id, role='user', message=message)
        db.session.add(user_msg)
        db.session.commit()
        
        # Generate AI response (basic implementation)
        ai_response = generate_ai_response(user, message)
        
        # Save AI response
        ai_msg = ChatMessage(user_id=user_id, role='assistant', message=ai_response)
        db.session.add(ai_msg)
        db.session.commit()
        
        return jsonify({
            'user_message': message,
            'assistant_response': ai_response,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get chat message history"""
    try:
        user_id = get_jwt_identity()
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at).all()
        
        history = [{
            'id': msg.id,
            'role': msg.role,
            'message': msg.message,
            'created_at': msg.created_at.isoformat()
        } for msg in messages]
        
        return jsonify(history), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_ai_response(user, message):
    """Generate AI response based on user message and profile"""
    # TODO: Integrate with Google Generative AI or similar
    # For now, return placeholder response
    
    user_context = f"""
    User: {user.name}, Age: {user.age}
    Health Goals: Sleep {user.sleep_goal_hours}h, Exercise {user.exercise_goal_minutes}min
    Stress Level: {user.job_stress_level}
    """
    
    responses = {
        'sleep': 'Based on your profile, aim for consistent sleep at 10 PM. This helps with your stress management.',
        'exercise': f'Try to get at least {user.exercise_goal_minutes} minutes of exercise daily. Walking, yoga, or any activity you enjoy works!',
        'stress': f'Your job stress is {user.job_stress_level}. Consider meditation, deep breathing, or taking breaks.',
        'medication': 'Have you taken all your medications today? I can help you track them.',
        'water': 'Remember to drink water regularly! Aim for 8-10 glasses daily.',
        'mood': 'How are you feeling today? Let\'s work on improving your wellbeing.',
    }
    
    message_lower = message.lower()
    for key, response in responses.items():
        if key in message_lower:
            return response
    
    return f"I understand you're asking about your health. Based on your profile, I recommend following your daily schedule and logging your activities. How can I help you today?"


# ==================== DAILY GOALS & PROGRESS ====================

@app.route('/api/daily-goals/today', methods=['GET'])
@jwt_required()
def get_today_goals():
    """Get today's goals and progress"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        today = datetime.utcnow().date()
        
        goals = DailyGoal.query.filter_by(user_id=user_id, goal_date=today).all()
        
        if not goals:
            # Generate today's goals if they don't exist
            goals = generate_daily_goals(user, today)
        
        goals_list = [{
            'id': goal.id,
            'goal_type': goal.goal_type,
            'target_value': goal.target_value,
            'current_value': goal.current_value,
            'unit': goal.unit,
            'completed': goal.completed,
            'progress_percent': (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0
        } for goal in goals]
        
        completed_count = sum(1 for g in goals if g.completed)
        total_count = len(goals)
        
        return jsonify({
            'goals': goals_list,
            'summary': {
                'total_goals': total_count,
                'completed_goals': completed_count,
                'completion_percentage': (completed_count / total_count * 100) if total_count > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_daily_goals(user, date):
    """Generate daily goals based on user profile"""
    goals = [
        DailyGoal(user_id=user.id, goal_date=date, goal_type='water', 
                 target_value=8, unit='liters'),
        DailyGoal(user_id=user.id, goal_date=date, goal_type='sleep',
                 target_value=user.sleep_goal_hours or 8, unit='hours'),
        DailyGoal(user_id=user.id, goal_date=date, goal_type='exercise',
                 target_value=user.exercise_goal_minutes or 30, unit='minutes'),
        DailyGoal(user_id=user.id, goal_date=date, goal_type='meditation',
                 target_value=10, unit='minutes'),
        DailyGoal(user_id=user.id, goal_date=date, goal_type='medication',
                 target_value=user.medications.__len__(), unit='pills'),
    ]
    
    db.session.add_all(goals)
    db.session.commit()
    return goals


@app.route('/api/daily-goals/<int:goal_id>/progress', methods=['PUT'])
@jwt_required()
def update_goal_progress(goal_id):
    """Update progress on a daily goal"""
    try:
        user_id = get_jwt_identity()
        goal = DailyGoal.query.filter_by(id=goal_id, user_id=user_id).first()
        
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        data = request.get_json()
        goal.current_value = data.get('current_value', goal.current_value)
        
        if goal.current_value >= goal.target_value:
            goal.completed = True
        
        db.session.commit()
        
        return jsonify({'message': 'Goal progress updated', 'completed': goal.completed}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
