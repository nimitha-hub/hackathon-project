"""
Integration Guide for HealthPal Backend
Detailed integration instructions for advanced features
"""

# ==================== INTEGRATING ADVANCED FEATURES ====================

"""
To use the advanced features module, add these imports and endpoints to app.py:
"""

# Add to imports in app.py:
# from advanced_features import (
#     get_nutrition_suggestions,
#     generate_weekly_nutrition_plan,
#     generate_health_insights,
#     generate_personalized_daily_schedule,
#     get_personalized_health_goals
# )

"""
NEW ENDPOINTS TO ADD:
"""

# Add these route examples to app.py:

NUTRITION_ENDPOINTS = """
@app.route('/api/nutrition/suggestions', methods=['GET'])
@jwt_required()
def get_nutrition_suggestions_endpoint():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Get today's health data
        today = datetime.utcnow().date()
        checkin = HealthCheckIn.query.filter_by(
            user_id=user_id, 
            check_in_date=today
        ).first()
        
        user_profile = {
            'age': user.age,
            'weight_kg': user.weight_kg,
            'height_cm': user.height_cm,
            'dietary_restrictions': user.dietary_restrictions,
            'allergies': user.allergies,
            'blood_pressure_sys': user.blood_pressure_sys,
            'blood_pressure_dia': user.blood_pressure_dia,
        }
        
        health_data = {
            'stress_level': checkin.stress_level if checkin else 5,
            'sleep_hours': checkin.sleep_hours if checkin else 0,
            'exercise_minutes': checkin.exercise_minutes if checkin else 0,
        } if checkin else {}
        
        from advanced_features import get_nutrition_suggestions
        suggestions = get_nutrition_suggestions(user_profile, health_data)
        
        return jsonify(suggestions), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/nutrition/weekly-plan', methods=['GET'])
@jwt_required()
def get_weekly_nutrition_plan_endpoint():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        user_profile = {
            'age': user.age,
            'weight_kg': user.weight_kg,
            'height_cm': user.height_cm,
            'dietary_restrictions': user.dietary_restrictions,
            'exercise_goal_minutes': user.exercise_goal_minutes,
        }
        
        health_data = {}
        
        from advanced_features import generate_weekly_nutrition_plan
        plan = generate_weekly_nutrition_plan(user_profile, health_data)
        
        return jsonify(plan), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""

INSIGHTS_ENDPOINTS = """
@app.route('/api/health/insights', methods=['GET'])
@jwt_required()
def get_health_insights_endpoint():
    try:
        user_id = get_jwt_identity()
        
        from advanced_features import generate_health_insights
        insights = generate_health_insights(user_id, db, User, HealthCheckIn)
        
        return jsonify(insights), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/schedule/daily', methods=['GET'])
@jwt_required()
def get_daily_schedule_endpoint():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        user_profile = {
            'age': user.age,
            'sleep_goal_hours': user.sleep_goal_hours,
            'exercise_goal_minutes': user.exercise_goal_minutes,
            'job_stress_level': user.job_stress_level,
            'has_menstrual_cycle': user.has_menstrual_cycle,
            'menstrual_cycle_day': user.menstrual_cycle_day,
        }
        
        today = datetime.utcnow().date()
        checkin = HealthCheckIn.query.filter_by(
            user_id=user_id,
            check_in_date=today
        ).first()
        
        health_data = {
            'mood': checkin.mood if checkin else None,
            'stress_level': checkin.stress_level if checkin else 5,
        } if checkin else {}
        
        from advanced_features import generate_personalized_daily_schedule
        schedule = generate_personalized_daily_schedule(user_profile, health_data)
        
        return jsonify(schedule), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health/goals', methods=['GET'])
@jwt_required()
def get_health_goals_endpoint():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        user_profile = {
            'sleep_goal_hours': user.sleep_goal_hours,
            'exercise_goal_minutes': user.exercise_goal_minutes,
            'job_stress_level': user.job_stress_level,
            'medications': user.medications,
        }
        
        today = datetime.utcnow().date()
        checkin = HealthCheckIn.query.filter_by(
            user_id=user_id,
            check_in_date=today
        ).first()
        
        current_health_status = {
            'current_sleep': checkin.sleep_hours if checkin else 0,
            'water_today': checkin.water_intake_liters if checkin else 0,
            'exercise_today': checkin.exercise_minutes if checkin else 0,
            'meditation_today': checkin.meditation_minutes if checkin else 0,
        } if checkin else {}
        
        from advanced_features import get_personalized_health_goals
        goals = get_personalized_health_goals(user_profile, current_health_status)
        
        return jsonify(goals), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""

# ==================== GOOGLE AI INTEGRATION ====================

GOOGLE_AI_SETUP = """
To integrate Google Generative AI for better chat responses:

1. Get API key from: https://makersuite.google.com/app/apikey

2. Add to requirements.txt:
   google-generativeai==0.3.0

3. Update .env:
   GOOGLE_API_KEY=your-api-key-here

4. Replace generate_ai_response function in app.py:

import google.generativeai as genai

def generate_ai_response_with_ai(user, message):
    '''Generate AI response using Google Generative AI'''
    try:
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        user_context = f'''
        You are a health assistant named HealthPal. 
        User: {user.name}, Age: {user.age}
        Health Goals: Sleep {user.sleep_goal_hours}h, Exercise {user.exercise_goal_minutes}min
        Stress Level: {user.job_stress_level}
        
        Provide personalized health advice based on their profile.
        '''
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_context + "\n\nUser: " + message)
        
        return response.text
    except Exception as e:
        print(f"Error with AI: {e}")
        return "I'm here to help with your health! Ask me anything about your wellness goals."
"""

# ==================== SCHEDULER INTEGRATION ====================

SCHEDULER_SETUP = """
To enable automated reminders and weekly reports:

1. In app.py, add at the bottom before app.run():

from utilities import init_scheduler

# Initialize background scheduler
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Start background scheduler
    scheduler = init_scheduler(app, db)
    
    try:
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        scheduler.shutdown()

2. Make sure email is configured in .env:
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password

3. Scheduled tasks:
   - Weekly reports: Every Sunday at 9 AM
   - Daily reminders: 7 AM and 7 PM
   - Motivation: Every day at 8 AM

4. Monitor logs for scheduler:
   - Look for "Background scheduler started!" message
   - Check console for sent email confirmations
"""

# ==================== DEPLOYMENT GUIDE ====================

DEPLOYMENT_HEROKU = """
To deploy HealthPal to Heroku:

1. Install Heroku CLI:
   https://devcenter.heroku.com/articles/heroku-cli

2. Create Heroku app:
   heroku create your-app-name
   
3. Add Procfile to backend:
   web: gunicorn app:app

4. Add requirements:
   pip install gunicorn

5. Update requirements.txt:
   pip freeze > requirements.txt

6. Deploy:
   git push heroku main

7. View logs:
   heroku logs --tail

8. Set environment variables:
   heroku config:set JWT_SECRET_KEY=your-secret
   heroku config:set SENDER_EMAIL=your-email
   heroku config:set SENDER_PASSWORD=your-password
"""

DEPLOYMENT_RAILWAY = """
To deploy to Railway (easier than Heroku):

1. Go to 
2. Click "New Project"
3. Connect GitHub repo
4. Select backend directory
5. Add environment variables in Railway dashboard
6. Deploy!

Railway automatically detects Flask apps.
"""

# ==================== DATABASE OPTIMIZATION ====================

DATABASE_OPTIMIZATION = """
For production, replace SQLite with PostgreSQL:

1. Install PostgreSQL driver:
   pip install psycopg2-binary

2. Update app.py:
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
       'DATABASE_URL',
       'postgresql://user:password@localhost/healthpal'
   )

3. On Heroku:
   heroku addons:create heroku-postgresql:hobby-dev
   
4. For other platforms:
   Use managed PostgreSQL service
   Update connection string in environment
"""

# ==================== FRONTEND OPTIMIZATION ====================

FRONTEND_BUILD = """
To build optimized frontend for production:

1. Create .env file in frontend:
   REACT_APP_API_URL=https://your-backend-url.com

2. Build:
   npm run build

3. This creates optimized production build in build/ folder

4. Deploy to:
   - Vercel (recommended for React)
   - Netlify
   - GitHub Pages
   - AWS S3 + CloudFront
"""

# ==================== MONITORING & LOGGING ====================

MONITORING = """
Add comprehensive logging to production:

1. Install:
   pip install python-json-logger

2. Add to app.py:
   import logging
   from pythonjsonlogger import jsonlogger

   logHandler = logging.StreamHandler()
   formatter = jsonlogger.JsonFormatter()
   logHandler.setFormatter(formatter)
   logger = logging.getLogger()
   logger.addHandler(logHandler)
   logger.setLevel(logging.INFO)

3. Monitor with:
   - Sentry (https://sentry.io/) for error tracking
   - DataDog or New Relic for performance
   - CloudWatch for AWS deployments
"""

# ==================== SECURITY CHECKLIST ====================

SECURITY = """
Before production:

✅ Change JWT_SECRET_KEY to strong random value
✅ Hash passwords using bcrypt (not plain text!)
✅ Enable HTTPS only
✅ Set CORS origins properly
✅ Add rate limiting
✅ Validate all user inputs
✅ Use environment variables for secrets
✅ Add CSRF protection
✅ Implement request logging
✅ Regular security audits

Example password hashing:
    from werkzeug.security import generate_password_hash
    
    user.password_hash = generate_password_hash(password)
"""

if __name__ == "__main__":
    print("Integration guide loaded. See docstrings above for instructions.")
