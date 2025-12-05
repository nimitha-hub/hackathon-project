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
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Allow all origins for now
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

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
                
                # Build detailed context prompt with user health data
                context = "You are an expert health and fitness assistant. "
                
                user_stats = []
                if user.nickname:
                    user_stats.append(f"Name: {user.nickname}")
                if user.height_cm and user.weight_kg:
                    bmi = user.weight_kg / ((user.height_cm / 100) ** 2)
                    user_stats.append(f"Height: {user.height_cm}cm, Weight: {user.weight_kg}kg, BMI: {bmi:.1f}")
                    if bmi < 18.5:
                        user_stats.append("Status: Underweight")
                    elif bmi < 25:
                        user_stats.append("Status: Normal weight")
                    elif bmi < 30:
                        user_stats.append("Status: Overweight")
                    else:
                        user_stats.append("Status: Obese")
                        
                if user.blood_type:
                    user_stats.append(f"Blood type: {user.blood_type}")
                if user.blood_pressure_sys and user.blood_pressure_dia:
                    user_stats.append(f"Blood pressure: {user.blood_pressure_sys}/{user.blood_pressure_dia}")
                if user.blood_sugar_fasting:
                    user_stats.append(f"Fasting blood sugar: {user.blood_sugar_fasting}")
                if user.sleep_goal_hours:
                    user_stats.append(f"Sleep goal: {user.sleep_goal_hours} hours")
                    
                if user_stats:
                    context += f"User profile: {', '.join(user_stats)}. "
                
                context += """
                
                You are an enthusiastic, supportive health coach. Provide detailed, personalized advice:
                
                For diet questions:
                - Suggest specific meals with ingredients and portions
                - Include breakfast, lunch, dinner, and snacks
                - Mention calories and macros
                - Give a full week plan if asked
                - Consider their BMI and health goals
                
                For fitness questions:
                - Design detailed workout routines with specific exercises
                - Include sets, reps, rest times
                - Provide 7-day weekly schedules
                - Mix cardio, strength, flexibility
                - Adapt to their fitness level
                
                For sleep/health questions:
                - Give specific, actionable tips
                - Create schedules and routines
                - Be motivating and encouraging
                
                Always be comprehensive, practical, and enthusiastic. Use emojis occasionally. Format with clear sections and bullet points."""
                
                # Generate AI response based on provider
                if ai_provider == 'openai':
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": context},
                            {"role": "user", "content": message}
                        ],
                        max_tokens=800,  # Increased for detailed responses
                        temperature=0.7
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
            'sleep': '''Here's your personalized sleep schedule! 🌙

**Optimal Sleep Routine:**
• 10:00 PM - Wind down (dim lights, no screens)
• 10:30 PM - Bedtime routine (shower, read, meditate)
• 11:00 PM - Lights out
• 7:00 AM - Wake up naturally

**Sleep Tips:**
✓ Keep bedroom cool (65-68°F)
✓ Use blackout curtains
✓ No caffeine after 2 PM
✓ Exercise earlier in the day
✓ Practice 4-7-8 breathing before bed

Stick to this for 2 weeks and you'll feel amazing!''',

            'diet': '''Let me create a nutrition plan for you! 🥗

**Sample Day (2000 calories):**

**Breakfast (400 cal):**
• 2 eggs scrambled with spinach
• 1 slice whole grain toast with avocado
• Green tea

**Snack (150 cal):**
• Greek yogurt with berries

**Lunch (500 cal):**
• Grilled chicken breast (6oz)
• Quinoa (1 cup)
• Mixed vegetable salad with olive oil

**Snack (200 cal):**
• Apple with almond butter (2 tbsp)

**Dinner (550 cal):**
• Baked salmon (6oz)
• Sweet potato (medium)
• Steamed broccoli

**Evening Snack (200 cal):**
• Protein shake or cottage cheese

💧 Drink 8-10 glasses of water daily!''',

            'weight': '''Here's your weight loss strategy! 💪

**To Lose Weight Safely:**

**Diet Changes:**
• Reduce calories by 500/day (1 lb/week loss)
• Eat protein with every meal
• Fill half your plate with vegetables
• Avoid sugary drinks and processed foods
• Track your food intake

**Exercise Plan:**
• 30 min cardio, 5 days/week
• Strength training 3 days/week
• 10,000 steps daily

**Weekly Meal Prep:**
• Sunday: Grill chicken breasts, cook quinoa
• Portion vegetables for the week
• Prepare healthy snacks

**Sample Meals:**
• Breakfast: Oatmeal + protein powder + berries
• Lunch: Chicken + veggies + brown rice
• Dinner: Fish + salad + sweet potato

You've got this! 🎯''',

            'exercise': '''Your personalized workout plan! 🏋️

**7-Day Fitness Schedule:**

**Monday - Upper Body:**
• Warm-up: 5 min jumping jacks
• Push-ups: 3×15
• Dumbbell rows: 3×12
• Shoulder press: 3×10
• Bicep curls: 3×12
• Tricep dips: 3×10

**Tuesday - Cardio:**
• 30 min running/cycling
• Intervals: 2 min fast, 2 min slow

**Wednesday - Lower Body:**
• Squats: 4×15
• Lunges: 3×12 each leg
• Leg press: 3×15
• Calf raises: 3×20
• Glute bridges: 3×15

**Thursday - Active Recovery:**
• Yoga or stretching: 30 min
• Light walk: 20 min

**Friday - Full Body Circuit:**
• Burpees: 3×10
• Mountain climbers: 3×20
• Planks: 3×45 sec
• Jump squats: 3×15

**Saturday - Core & Cardio:**
• 20 min HIIT
• Abs workout: 15 min

**Sunday - Rest Day:**
• Light stretching only

Remember to warm up and cool down! 🔥''',

            'workout': '''Your complete workout routine! 💪

**Beginner-Friendly Full Body Workout:**

**Warm-Up (5 minutes):**
• Jumping jacks: 30 sec
• Arm circles: 30 sec
• Leg swings: 30 sec
• Light jog in place: 2 min

**Main Workout (30 minutes):**

1. **Bodyweight Squats**
   - 3 sets × 15 reps
   - Rest 60 sec

2. **Push-Ups** (knees if needed)
   - 3 sets × 10 reps
   - Rest 60 sec

3. **Walking Lunges**
   - 3 sets × 10 each leg
   - Rest 60 sec

4. **Plank Hold**
   - 3 sets × 30 sec
   - Rest 45 sec

5. **Dumbbell Rows**
   - 3 sets × 12 reps
   - Rest 60 sec

**Cool Down (5 minutes):**
• Stretching all major muscles
• Deep breathing

Do this 3× per week! You'll see results in 4 weeks! 🎯''',

            'medication': '''Medication Management Tips! 💊

**Best Practices:**
• Set phone reminders for each dose
• Use a pill organizer for the week
• Take at same time daily
• Keep a medication log
• Store properly (cool, dry place)

**Important:**
✓ Never skip doses
✓ Don't stop without doctor approval
✓ Report side effects immediately
✓ Keep track of refills
✓ Avoid interactions (check with pharmacist)

**Reminder System:**
• Morning meds: 8 AM alarm
• Evening meds: 8 PM alarm
• Weekly refill check: Sunday

Stay consistent for best results!''',

            'water': '''Stay Hydrated! 💧

**Daily Water Goal: 8-10 glasses (64-80 oz)**

**Hydration Schedule:**
• Wake up: 16 oz (2 glasses)
• Mid-morning: 8 oz
• Before lunch: 8 oz
• Afternoon: 16 oz
• Before dinner: 8 oz
• Evening: 8 oz

**Tips to Drink More:**
✓ Carry a reusable water bottle
✓ Add lemon/cucumber for flavor
✓ Drink a glass before each meal
✓ Set hourly reminders
✓ Track with an app

**Signs You're Hydrated:**
• Clear/pale yellow urine
• Good energy levels
• Moist lips and skin

Keep that bottle handy! 🌊'''
        }
        
        response_text = '''I'm your HealMate assistant! 🌟 I can help you with:

📊 **Diet Plans** - Personalized meal plans with calories
🏋️ **Workout Routines** - Custom fitness programs
😴 **Sleep Schedules** - Optimize your rest
💊 **Medication Reminders** - Stay on track
💧 **Hydration Goals** - Water intake tips
❤️ **Health Advice** - General wellness guidance

Ask me anything specific like:
• "Create a diet plan for me"
• "I need a workout routine"
• "How can I lose weight?"
• "Give me a sleep schedule"

What would you like help with today?'''
        
        message_lower = message.lower()
        for keyword, response in fallback_responses.items():
            if keyword in message_lower:
                response_text = response
                break
        
        return jsonify({
            'assistant_response': response_text,
            'message': 'Chat response (fallback mode - set OPENAI_API_KEY for AI-powered responses)'
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    return jsonify([]), 200

# ==================== WORKOUT & DIET PLAN ROUTES ====================

@app.route('/api/workout-plan', methods=['GET'])
@jwt_required()
def get_workout_plan():
    """Generate personalized workout plan"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Build user context
        user_info = []
        if user.height_cm and user.weight_kg:
            bmi = user.weight_kg / ((user.height_cm / 100) ** 2)
            user_info.append(f"BMI: {bmi:.1f}")
            fitness_level = "beginner" if bmi > 30 else "intermediate" if bmi > 25 else "advanced"
        else:
            fitness_level = "intermediate"
        
        if AI_AVAILABLE:
            try:
                prompt = f"""Create a detailed 7-day workout plan for a {fitness_level} level person.
                User stats: {', '.join(user_info) if user_info else 'Not provided'}
                
                Include:
                - Day-by-day breakdown (Monday-Sunday)
                - Specific exercises with sets, reps, and rest periods
                - Warm-up and cool-down for each day
                - Mix of cardio, strength, and flexibility
                - Rest days
                - Progressive difficulty
                
                Format clearly with bullet points."""
                
                if ai_provider == 'openai':
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a certified fitness trainer."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.7
                    )
                    workout_plan = response.choices[0].message.content
                elif ai_provider == 'google':
                    response = ai_model.generate_content(prompt)
                    workout_plan = response.text
                else:
                    raise Exception("No AI available")
                
                return jsonify({
                    'workout_plan': workout_plan,
                    'fitness_level': fitness_level
                }), 200
                
            except Exception as e:
                print(f"Workout plan error: {e}")
        
        # Fallback workout plan
        fallback_plan = """
**Weekly Workout Plan (Intermediate Level)**

**Monday - Upper Body Strength**
• Warm-up: 5 min light cardio
• Push-ups: 3 sets of 10-15 reps
• Dumbbell rows: 3 sets of 12 reps
• Shoulder press: 3 sets of 10 reps
• Planks: 3 sets of 30 seconds

**Tuesday - Cardio**
• 30 minutes moderate-intensity jogging or cycling
• Stretching: 10 minutes

**Wednesday - Lower Body**
• Squats: 3 sets of 15 reps
• Lunges: 3 sets of 10 reps per leg
• Leg raises: 3 sets of 12 reps
• Calf raises: 3 sets of 15 reps

**Thursday - Rest/Active Recovery**
• Light walking or yoga: 20 minutes

**Friday - Full Body Circuit**
• Burpees: 3 sets of 8 reps
• Mountain climbers: 3 sets of 15 reps
• Jumping jacks: 3 sets of 20 reps
• Core exercises: 15 minutes

**Saturday - Flexibility & Core**
• Yoga or Pilates: 45 minutes
• Focus on stretching and breathing

**Sunday - Rest**
• Complete rest or gentle stretching

**Tips:**
- Stay hydrated
- Listen to your body
- Progress gradually
- Get adequate sleep
"""
        
        return jsonify({
            'workout_plan': fallback_plan,
            'fitness_level': fitness_level,
            'message': 'Fallback plan - configure AI for personalized plans'
        }), 200
        
    except Exception as e:
        print(f"Workout plan error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/diet-plan', methods=['GET'])
@jwt_required()
def get_diet_plan():
    """Generate personalized diet plan"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Calculate calorie needs
        user_info = []
        if user.height_cm and user.weight_kg:
            bmi = user.weight_kg / ((user.height_cm / 100) ** 2)
            # Rough BMR calculation (assuming age 30, moderate activity)
            bmr = 10 * user.weight_kg + 6.25 * user.height_cm - 5 * 30
            daily_calories = int(bmr * 1.5)  # Moderate activity multiplier
            user_info.append(f"Target calories: {daily_calories}/day")
            user_info.append(f"BMI: {bmi:.1f}")
        else:
            daily_calories = 2000  # Default
        
        if AI_AVAILABLE:
            try:
                prompt = f"""Create a detailed 7-day meal plan.
                User stats: {', '.join(user_info) if user_info else f'Target: {daily_calories} calories/day'}
                
                For each day provide:
                - Breakfast (with calories and macros)
                - Mid-morning snack
                - Lunch (with calories and macros)
                - Afternoon snack
                - Dinner (with calories and macros)
                
                Include:
                - Specific portions
                - Variety of healthy foods
                - Balanced macros (protein, carbs, fats)
                - Easy-to-prepare meals
                - Hydration tips
                
                Format clearly by day and meal."""
                
                if ai_provider == 'openai':
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a certified nutritionist."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1200,
                        temperature=0.7
                    )
                    diet_plan = response.choices[0].message.content
                elif ai_provider == 'google':
                    response = ai_model.generate_content(prompt)
                    diet_plan = response.text
                else:
                    raise Exception("No AI available")
                
                return jsonify({
                    'diet_plan': diet_plan,
                    'daily_calories': daily_calories
                }), 200
                
            except Exception as e:
                print(f"Diet plan error: {e}")
        
        # Fallback diet plan
        fallback_plan = f"""
**Weekly Meal Plan ({daily_calories} calories/day)**

**Monday**
• Breakfast: Oatmeal with berries and nuts (350 cal)
• Snack: Greek yogurt (150 cal)
• Lunch: Grilled chicken salad with olive oil (450 cal)
• Snack: Apple with almond butter (200 cal)
• Dinner: Baked salmon with vegetables and quinoa (550 cal)

**Tuesday**
• Breakfast: Scrambled eggs with whole wheat toast (400 cal)
• Snack: Protein shake (200 cal)
• Lunch: Turkey wrap with vegetables (450 cal)
• Snack: Carrot sticks with hummus (150 cal)
• Dinner: Stir-fried tofu with brown rice (500 cal)

**Wednesday**
• Breakfast: Smoothie bowl with granola (380 cal)
• Snack: Mixed nuts (180 cal)
• Lunch: Quinoa bowl with chickpeas (480 cal)
• Snack: Banana (100 cal)
• Dinner: Grilled chicken with sweet potato (560 cal)

**Thursday**
• Breakfast: Whole grain pancakes with fruit (400 cal)
• Snack: Cottage cheese (150 cal)
• Lunch: Lentil soup with bread (420 cal)
• Snack: Trail mix (200 cal)
• Dinner: Baked fish with roasted vegetables (530 cal)

**Friday**
• Breakfast: Avocado toast with egg (420 cal)
• Snack: Protein bar (180 cal)
• Lunch: Buddha bowl with tahini (500 cal)
• Snack: Orange (80 cal)
• Dinner: Lean beef with salad (520 cal)

**Saturday**
• Breakfast: Greek yogurt parfait (350 cal)
• Snack: Celery with peanut butter (170 cal)
• Lunch: Veggie burger with sweet potato fries (480 cal)
• Snack: Berries (100 cal)
• Dinner: Shrimp pasta with vegetables (600 cal)

**Sunday**
• Breakfast: Whole grain cereal with milk (350 cal)
• Snack: Cheese and crackers (180 cal)
• Lunch: Chicken Caesar salad (450 cal)
• Snack: Pear (100 cal)
• Dinner: Baked chicken with quinoa (520 cal)

**General Tips:**
- Drink 8-10 glasses of water daily
- Adjust portions based on hunger
- Include vegetables with every meal
- Limit processed foods
- Meal prep on weekends
"""
        
        return jsonify({
            'diet_plan': fallback_plan,
            'daily_calories': daily_calories,
            'message': 'Fallback plan - configure AI for personalized plans'
        }), 200
        
    except Exception as e:
        print(f"Diet plan error: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== EMAIL ROUTE (SIMPLIFIED) ====================

@app.route('/api/send-email', methods=['POST'])
@jwt_required()
def send_email():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.email:
            return jsonify({'error': 'User email not found'}), 404
        
        # Calculate weekly stats (mock data for demo)
        weekly_stats = {
            'sleep_hours': 52,  # 7.4 hours avg per day
            'water_intake': 48,  # 6.8 glasses per day
            'exercise_minutes': 210,  # 30 min per day
            'meditation_minutes': 70,  # 10 min per day
            'medication_adherence': 95,  # 95% taken on time
            'meals_completed': 19,  # out of 21
            'stress_level': 'Low',
            'mood': 'Positive'
        }
        
        # Create email content
        subject = f"HealMate Weekly Health Report - {user.name}"
        
        body = f"""
Hello {user.name}! 👋

Here's your weekly health summary from HealMate:

📊 WEEKLY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💤 Sleep: {weekly_stats['sleep_hours']} hours total (avg 7.4h/day)
💧 Water: {weekly_stats['water_intake']} glasses (avg 6.8/day) 
🏃 Exercise: {weekly_stats['exercise_minutes']} minutes total
🧘 Meditation: {weekly_stats['meditation_minutes']} minutes total
💊 Medication: {weekly_stats['medication_adherence']}% adherence
🍽️ Meals: {weekly_stats['meals_completed']}/21 completed
😊 Mood: {weekly_stats['mood']}
😌 Stress: {weekly_stats['stress_level']}

🎯 GOALS ACHIEVED THIS WEEK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Maintained consistent sleep schedule
✅ Met daily water intake goal 6/7 days
✅ Completed all medication doses on time
✅ Exercised 5 days this week
✅ Logged meals regularly

💡 PERSONALIZED RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Great job on medication adherence! Keep it up! 💊
• Try to increase water intake by 1 more glass per day 💧
• Consider adding 10 more minutes of exercise 🏃
• Your sleep pattern is excellent - maintain it! 😴

📈 PROGRESS TRENDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sleep: ↗️ Improving (+30 min vs last week)
Water: ➡️ Stable
Exercise: ↗️ Improving (+45 min vs last week)
Mood: ↗️ Improving

🎉 Keep up the great work! You're making excellent progress on your health journey.

Stay healthy,
The HealMate Team 💚

---
View your detailed dashboard: {os.environ.get('FRONTEND_URL', 'https://healmate.app')}
"""
        
        # Send email using SMTP
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        
        if not sender_email or not sender_password:
            return jsonify({'error': 'Email configuration missing'}), 500
        
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user.email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return jsonify({
            'message': 'Weekly health report sent successfully!',
            'sent_to': user.email
        }), 200
        
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

# ==================== INITIALIZATION ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized!")
    
    print("Starting HealMate Backend (Simplified Mode)...")
    print("Backend running on http://localhost:5000")
    app.run(debug=False, port=5000, use_reloader=False, threaded=True)
