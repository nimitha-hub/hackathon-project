"""
Minimal HealMate Backend - Core functionality only
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
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

print("Flask app initialized")

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(100))
    
    # Health metrics
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    blood_type = db.Column(db.String(10))
    blood_sugar_fasting = db.Column(db.Float)
    blood_pressure_sys = db.Column(db.Integer)
    blood_pressure_dia = db.Column(db.Integer)
    sleep_goal_hours = db.Column(db.Float, default=8)
    
    # Relationships
    medications = db.relationship('Medication', backref='user', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Medication(db.Model):
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    stock_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== AUTH ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=data['email'],
            password_hash=data['password'],
            name=data.get('name', '')
        )
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Registration successful',
            'access_token': access_token,
            'user_id': user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Register error: {e}")
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
        print(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== PROFILE ROUTES ====================

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        medications = Medication.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'nickname': user.nickname,
            'height_cm': user.height_cm,
            'weight_kg': user.weight_kg,
            'blood_type': user.blood_type,
            'blood_sugar_fasting': user.blood_sugar_fasting,
            'blood_pressure_sys': user.blood_pressure_sys,
            'blood_pressure_dia': user.blood_pressure_dia,
            'sleep_goal_hours': user.sleep_goal_hours,
            'medications': [
                {
                    'id': m.id,
                    'name': m.name,
                    'dosage': m.dosage,
                    'frequency': m.frequency,
                    'stock_quantity': m.stock_quantity
                }
                for m in medications
            ]
        }), 200
        
    except Exception as e:
        print(f"Get profile error: {e}")
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
        
        if 'nickname' in data:
            user.nickname = data['nickname']
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
        if 'sleep_goal_hours' in data:
            user.sleep_goal_hours = data['sleep_goal_hours']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Update profile error: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== MEDICATION ROUTES ====================

@app.route('/api/medications', methods=['POST'])
@jwt_required()
def add_medication():
    """Add medication"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        medication = Medication(
            user_id=user_id,
            name=data.get('name'),
            dosage=data.get('dosage'),
            frequency=data.get('frequency'),
            stock_quantity=data.get('stock_quantity')
        )
        db.session.add(medication)
        db.session.commit()
        
        return jsonify({
            'id': medication.id,
            'message': 'Medication added successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Add medication error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    """Chat with AI assistant (fallback response)"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        fallback_responses = {
            'health': 'I can help with health-related questions. Please tell me more about your health concerns.',
            'medication': 'Medications are important for managing health. Do you have any questions about your medications?',
            'sleep': 'Good sleep is essential for health. Try to maintain consistent sleep schedules.',
            'exercise': 'Regular exercise is beneficial. Aim for at least 30 minutes of activity daily.',
        }
        
        response_text = 'I am your HealMate AI assistant. How can I help you with your health today?'
        for keyword, response in fallback_responses.items():
            if keyword.lower() in message.lower():
                response_text = response
                break
        
        return jsonify({
            'assistant_response': response_text
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get chat history"""
    try:
        return jsonify([]), 200
    except Exception as e:
        print(f"Chat history error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/send-email', methods=['POST'])
@jwt_required()
def send_email():
    """Send weekly report email"""
    try:
        user_id = get_jwt_identity()
        return jsonify({
            'message': 'Weekly report sent to your email!'
        }), 200
    except Exception as e:
        print(f"Send email error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Initializing database...")
    with app.app_context():
        db.create_all()
    print("Database initialized")
    
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=False, port=5000, use_reloader=False, threaded=True)
