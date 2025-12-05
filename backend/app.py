from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import sys
import traceback
from dotenv import load_dotenv

load_dotenv()

# Try to import AI libraries
AI_AVAILABLE = False
ai_provider = None

# Try OpenAI first (more stable on Python 3.14)
try:
    from openai import OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        AI_AVAILABLE = True
        ai_provider = 'openai'
        print("OpenAI configured successfully")
except Exception as e:
    print(f"OpenAI not available: {e}")

# Try Google AI as fallback
if not AI_AVAILABLE:
    try:
        import google.generativeai as genai
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            ai_model = genai.GenerativeModel('gemini-pro')
            AI_AVAILABLE = True
            ai_provider = 'google'
            print("Google AI configured successfully")
        else:
            print("No Google API key found")
    except Exception as e:
        print(f"Google AI not available: {e}")

if not AI_AVAILABLE:
    print("AI chat will use fallback responses - add OPENAI_API_KEY or fix Google AI")

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healmate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ==================== MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile fields
    nickname = db.Column(db.String(50))
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    blood_type = db.Column(db.String(10))
    blood_pressure_sys = db.Column(db.Integer)
    blood_pressure_dia = db.Column(db.Integer)
    blood_sugar_fasting = db.Column(db.Float)
    sleep_goal_hours = db.Column(db.Float)
    work_start_time = db.Column(db.String(10))
    work_end_time = db.Column(db.String(10))

# ==================== AUTH ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'message': 'User registered successfully'
        }), 201
    except Exception as e:
        print(f"Registration error: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.stderr.flush()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'message': 'Login successful'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PROFILE ROUTES ====================

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'nickname': user.nickname,
            'height_cm': user.height_cm,
            'weight_kg': user.weight_kg,
            'blood_type': user.blood_type,
            'blood_pressure_sys': user.blood_pressure_sys,
            'blood_pressure_dia': user.blood_pressure_dia,
            'blood_sugar_fasting': user.blood_sugar_fasting,
            'sleep_goal_hours': user.sleep_goal_hours,
            'work_start_time': user.work_start_time,
            'work_end_time': user.work_end_time,
            'medications': []  # Simplified for now
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update profile fields
        user.nickname = data.get('nickname', user.nickname)
        user.height_cm = data.get('height_cm', user.height_cm)
        user.weight_kg = data.get('weight_kg', user.weight_kg)
        user.blood_type = data.get('blood_type', user.blood_type)
        user.blood_pressure_sys = data.get('blood_pressure_sys', user.blood_pressure_sys)
        user.blood_pressure_dia = data.get('blood_pressure_dia', user.blood_pressure_dia)
        user.blood_sugar_fasting = data.get('blood_sugar_fasting', user.blood_sugar_fasting)
        user.sleep_goal_hours = data.get('sleep_goal_hours', user.sleep_goal_hours)
        user.work_start_time = data.get('work_start_time', user.work_start_time)
        user.work_end_time = data.get('work_end_time', user.work_end_time)
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CHAT ROUTES (SIMPLIFIED) ====================

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Try to use AI if available
        if AI_AVAILABLE:
            try:
                user_id = int(get_jwt_identity())
                user = User.query.get(user_id)
                
                # Build context prompt with user health data
                context = "You are a health assistant. "
                if user.nickname:
                    context += f"User name: {user.nickname}. "
                if user.height_cm and user.weight_kg:
                    bmi = user.weight_kg / ((user.height_cm / 100) ** 2)
                    context += f"BMI: {bmi:.1f}. "
                if user.blood_type:
                    context += f"Blood type: {user.blood_type}. "
                
                context += "Provide helpful, accurate health advice. Keep responses concise and friendly."
                
                # Generate AI response based on provider
                if ai_provider == 'openai':
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": context},
                            {"role": "user", "content": message}
                        ],
                        max_tokens=200
                    )
                    assistant_response = response.choices[0].message.content
                elif ai_provider == 'google':
                    prompt = f"{context}\n\nUser question: {message}"
                    response = ai_model.generate_content(prompt)
                    assistant_response = response.text
                else:
                    raise Exception("No AI provider available")
                
                return jsonify({
                    'assistant_response': assistant_response,
                    'message': f'AI response from {ai_provider}'
                }), 200
                
            except Exception as ai_error:
                print(f"AI generation error: {ai_error}")
                # Fall through to fallback
        
        # Fallback response
        fallback_responses = {
            'health': 'I can help with health-related questions. Please tell me more about your health concerns.',
            'medication': 'Medications are important for managing health. Do you have any questions about your medications?',
            'sleep': 'Good sleep is essential for health. Try to maintain consistent sleep schedules.',
            'exercise': 'Regular exercise is beneficial. Aim for at least 30 minutes of activity daily.',
            'diet': 'A balanced diet with plenty of fruits and vegetables supports overall health.',
            'water': 'Staying hydrated is important. Aim for 8 glasses of water per day.'
        }
        
        response_text = 'I am your HealMate assistant. How can I help you with your health today?'
        message_lower = message.lower()
        for keyword, response in fallback_responses.items():
            if keyword in message_lower:
                response_text = response
                break
        
        return jsonify({
            'assistant_response': response_text,
            'message': 'Chat response (fallback mode - set GOOGLE_API_KEY for AI)'
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    return jsonify([]), 200

# ==================== EMAIL ROUTE (SIMPLIFIED) ====================

@app.route('/api/send-email', methods=['POST'])
@jwt_required()
def send_email():
    return jsonify({'message': 'Email feature will be available once configured'}), 200

# ==================== INITIALIZATION ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized!")
    
    print("Starting HealMate Backend (Simplified Mode)...")
    print("Backend running on http://localhost:5000")
    app.run(debug=False, port=5000, use_reloader=False, threaded=True)
