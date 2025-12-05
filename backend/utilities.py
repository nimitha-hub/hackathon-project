"""
Scheduling, notifications, and email utilities for HealthPal
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== EMAIL CONFIGURATION ====================

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'healthpal@example.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'password')

def send_email(to_email, subject, body_html):
    """Send email notification"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        
        msg.attach(MIMEText(body_html, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# ==================== WEEKLY REPORT GENERATION ====================

def generate_weekly_report(user_id, db, User, HealthCheckIn, WeeklyHealthReport, Medication, MedicationIntake):
    """Generate weekly health summary report"""
    try:
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Get last 7 days of data
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=7)
        
        checkins = HealthCheckIn.query.filter(
            HealthCheckIn.user_id == user_id,
            HealthCheckIn.check_in_date >= start_date,
            HealthCheckIn.check_in_date <= end_date
        ).all()
        
        # Calculate metrics
        total_sleep = sum([c.sleep_hours or 0 for c in checkins])
        total_water = sum([c.water_intake_liters or 0 for c in checkins])
        total_exercise = sum([c.exercise_minutes or 0 for c in checkins])
        total_meditation = sum([c.meditation_minutes or 0 for c in checkins])
        
        # Medication adherence
        meds = Medication.query.filter_by(user_id=user_id).all()
        total_meds = sum(len(m.intake_logs) for m in meds)
        skipped_meds = sum(sum(1 for log in m.intake_logs if log.skipped) for m in meds)
        med_adherence = ((total_meds - skipped_meds) / total_meds * 100) if total_meds > 0 else 0
        
        # Calculate average mood
        moods = [c.mood for c in checkins if c.mood]
        avg_mood = moods[0] if moods else 'N/A'
        
        # Create report
        report = WeeklyHealthReport(
            user_id=user_id,
            week_start_date=start_date,
            week_end_date=end_date,
            total_sleep_hours=total_sleep,
            total_water_liters=total_water,
            medication_adherence_percent=med_adherence,
            exercise_minutes=total_exercise,
            meditation_minutes=total_meditation,
            goals_completed=len([c for c in checkins if c.sleep_hours >= user.sleep_goal_hours]),
            goals_missed=len([c for c in checkins if c.sleep_hours < user.sleep_goal_hours]),
            average_mood=avg_mood
        )
        
        db.session.add(report)
        db.session.commit()
        
        return report
        
    except Exception as e:
        print(f"Error generating weekly report: {e}")
        return None


def send_weekly_report(user_id, db, User, HealthCheckIn, WeeklyHealthReport, Medication, MedicationIntake):
    """Send weekly health report via email"""
    try:
        report = generate_weekly_report(user_id, db, User, HealthCheckIn, WeeklyHealthReport, Medication, MedicationIntake)
        user = User.query.get(user_id)
        
        if not report or not user:
            return False
        
        # Generate HTML email
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ padding: 20px; background: white; }}
                    .metric {{ margin: 15px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #667eea; }}
                    .metric-label {{ font-weight: bold; color: #333; }}
                    .metric-value {{ font-size: 1.5em; color: #667eea; margin-top: 5px; }}
                    .motivational {{ margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 5px; color: #2e7d32; }}
                    .footer {{ text-align: center; padding: 10px; color: #999; font-size: 0.9em; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Your Weekly Health Report</h1>
                        <p>Week of {report.week_start_date} to {report.week_end_date}</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hi {user.name}! 👋</h2>
                        <p>Here's your weekly health summary:</p>
                        
                        <div class="metric">
                            <div class="metric-label">💤 Sleep</div>
                            <div class="metric-value">{report.total_sleep_hours:.1f} hours</div>
                            <p>Goal: {user.sleep_goal_hours} hours/night</p>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">💧 Hydration</div>
                            <div class="metric-value">{report.total_water_liters:.1f} liters</div>
                            <p>Goal: 56 liters (8L per day)</p>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">💊 Medication Adherence</div>
                            <div class="metric-value">{report.medication_adherence_percent:.1f}%</div>
                            <p>Keep it up!</p>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">🏃 Exercise</div>
                            <div class="metric-value">{report.exercise_minutes} minutes</div>
                            <p>Goal: {user.exercise_goal_minutes} minutes/day</p>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">🧘 Meditation</div>
                            <div class="metric-value">{report.meditation_minutes} minutes</div>
                            <p>Great for mental health!</p>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-label">😊 Average Mood</div>
                            <div class="metric-value">{report.average_mood}</div>
                        </div>
                        
                        <div class="motivational">
                            <strong>💪 Keep Going!</strong><br/>
                            <p>You've completed {report.goals_completed} goals this week! 
                            Remember, small consistent steps lead to big health improvements. 
                            Keep tracking your health and stay committed to your wellness journey!</p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Keep taking care of your health! 🏥</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        success = send_email(
            user.email,
            "Your Weekly Health Report - HealthPal 🏥",
            html_content
        )
        
        if success:
            report.report_sent = True
            report.sent_at = datetime.utcnow()
            db.session.commit()
        
        return success
        
    except Exception as e:
        print(f"Error sending weekly report: {e}")
        return False


# ==================== REMINDER NOTIFICATIONS ====================

def send_medication_reminder(user_id, medication_id, db, Medication, User):
    """Send medication reminder"""
    try:
        medication = Medication.query.get(medication_id)
        user = User.query.get(user_id)
        
        if not medication or not user:
            return False
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>💊 Medication Reminder</h2>
                <p>Hi {user.name},</p>
                <p>It's time to take your medication:</p>
                <h3>{medication.name}</h3>
                <p><strong>Dosage:</strong> {medication.dosage}</p>
                <p><strong>Frequency:</strong> {medication.frequency}</p>
                <p><strong>Reason:</strong> {medication.reason}</p>
                <p>Please don't forget to take your medication on time for better health!</p>
                <p>Current stock: {medication.stock_quantity} remaining</p>
                
                {f'<p style="color: red; font-weight: bold;">⚠️ Warning: Stock is running low! Please refill soon.</p>' 
                 if medication.stock_quantity < medication.refill_threshold else ''}
            </body>
        </html>
        """
        
        return send_email(user.email, f"Medication Reminder: {medication.name}", html_content)
        
    except Exception as e:
        print(f"Error sending medication reminder: {e}")
        return False


def send_refill_reminder(user_id, medication_id, db, Medication, User):
    """Send medication refill reminder"""
    try:
        medication = Medication.query.get(medication_id)
        user = User.query.get(user_id)
        
        if not medication or not user:
            return False
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>⚠️ Medication Refill Reminder</h2>
                <p>Hi {user.name},</p>
                <p>Your medication stock is running low:</p>
                <h3>{medication.name}</h3>
                <p><strong>Current Stock:</strong> {medication.stock_quantity}</p>
                <p><strong>Refill Threshold:</strong> {medication.refill_threshold}</p>
                <p>Please refill your medication soon to avoid missing doses!</p>
            </body>
        </html>
        """
        
        return send_email(user.email, f"Refill Reminder: {medication.name}", html_content)
        
    except Exception as e:
        print(f"Error sending refill reminder: {e}")
        return False


def send_hydration_reminder(user_id, db, User):
    """Send water intake reminder"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>💧 Hydration Reminder</h2>
                <p>Hi {user.name},</p>
                <p>Don't forget to drink water! 💧</p>
                <p>Staying hydrated is essential for your health. Aim to drink 8-10 glasses of water today.</p>
                <p>Your current daily goal: 8 liters</p>
            </body>
        </html>
        """
        
        return send_email(user.email, "Hydration Reminder - HealthPal", html_content)
        
    except Exception as e:
        print(f"Error sending hydration reminder: {e}")
        return False


def send_screen_break_reminder(user_id, db, User):
    """Send screen break reminder"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>👁️ Screen Break Reminder</h2>
                <p>Hi {user.name},</p>
                <p>Time to take a break from your screen!</p>
                <p>Looking at screens for long periods can strain your eyes. Take a 5-10 minute break and look away from the screen.</p>
                <p>Try these activities during your break:</p>
                <ul>
                    <li>Look at something far away (20+ feet)</li>
                    <li>Do some gentle stretches</li>
                    <li>Get a glass of water</li>
                    <li>Take a short walk</li>
                </ul>
            </body>
        </html>
        """
        
        return send_email(user.email, "Screen Break Reminder - HealthPal", html_content)
        
    except Exception as e:
        print(f"Error sending screen break reminder: {e}")
        return False


def send_exercise_reminder(user_id, db, User):
    """Send exercise reminder"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>🏃 Exercise Reminder</h2>
                <p>Hi {user.name},</p>
                <p>Don't forget your daily exercise!</p>
                <p>Your daily goal: {user.exercise_goal_minutes} minutes</p>
                <p>Exercise benefits:</p>
                <ul>
                    <li>Improves cardiovascular health</li>
                    <li>Boosts mood and energy</li>
                    <li>Helps maintain healthy weight</li>
                    <li>Reduces stress</li>
                </ul>
                <p>Try any activity you enjoy - walking, yoga, dancing, swimming, or sports!</p>
            </body>
        </html>
        """
        
        return send_email(user.email, "Exercise Reminder - HealthPal", html_content)
        
    except Exception as e:
        print(f"Error sending exercise reminder: {e}")
        return False


def send_meditation_reminder(user_id, db, User):
    """Send meditation/mindfulness reminder"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False
        
        meditation_videos = [
            "https://www.youtube.com/watch?v=10us7-qGBKU",  # 10 min guided meditation
            "https://www.youtube.com/watch?v=Z6qt-FS1Nwc",  # 5 min breathing exercise
            "https://www.youtube.com/watch?v=LiKyJh-FGbI",  # 15 min body scan
        ]
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>🧘 Meditation Reminder</h2>
                <p>Hi {user.name},</p>
                <p>Take a moment for mindfulness and meditation!</p>
                <p>Even 5-10 minutes of meditation can:</p>
                <ul>
                    <li>Reduce stress and anxiety</li>
                    <li>Improve focus and clarity</li>
                    <li>Enhance emotional well-being</li>
                    <li>Better sleep quality</li>
                </ul>
                <p><strong>Try these guided meditations:</strong></p>
                <ul>
                    <li><a href="{meditation_videos[0]}">10 min Guided Meditation</a></li>
                    <li><a href="{meditation_videos[1]}">5 min Breathing Exercise</a></li>
                    <li><a href="{meditation_videos[2]}">15 min Body Scan Meditation</a></li>
                </ul>
            </body>
        </html>
        """
        
        return send_email(user.email, "Meditation Reminder - HealthPal 🧘", html_content)
        
    except Exception as e:
        print(f"Error sending meditation reminder: {e}")
        return False


def send_menstrual_cycle_reminder(user_id, db, User, HealthCheckIn):
    """Send menstrual cycle reminder"""
    try:
        user = User.query.get(user_id)
        if not user or not user.has_menstrual_cycle:
            return False
        
        html_content = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>🩸 Menstrual Cycle Reminder</h2>
                <p>Hi {user.name},</p>
                <p>This is a friendly reminder about your menstrual health.</p>
                <p><strong>Tips for this time:</strong></p>
                <ul>
                    <li>Stay hydrated - drink extra water</li>
                    <li>Get adequate iron-rich foods (spinach, beans, lean meat)</li>
                    <li>Gentle exercise like yoga or walking</li>
                    <li>Rest when needed</li>
                    <li>Track your symptoms in your health check-in</li>
                    <li>Take pain relief if needed</li>
                </ul>
                <p>Remember to log your menstrual flow and any symptoms in your daily check-in for better health insights.</p>
            </body>
        </html>
        """
        
        return send_email(user.email, "Menstrual Cycle Reminder - HealthPal", html_content)
        
    except Exception as e:
        print(f"Error sending menstrual cycle reminder: {e}")
        return False


# ==================== MOTIVATION MESSAGES ====================

def send_motivation_message(user_id, db, User):
    """Send motivational message to user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False
        
        motivation_messages = [
            "You're doing great! Keep up the consistency! 💪",
            "Every small step towards health is a victory! 🏆",
            "Your dedication to health is inspiring! Keep going! ✨",
            "Health is wealth - you're investing in your future! 💎",
            "Be proud of your progress! You're making positive changes! 🌟",
            "Your body will thank you for the care you're giving it! 🏃",
            "One day at a time - you've got this! 🎯",
            "Taking care of your health shows self-love! 💚",
        ]
        
        import random
        message = random.choice(motivation_messages)
        
        html_content = f"""
        <html>
            <body style="font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px;">
                <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto;">
                    <h2>Daily Motivation 💫</h2>
                    <p>Hi {user.name},</p>
                    <h3 style="color: #667eea; font-size: 1.3em;">{message}</h3>
                    <p>Keep tracking your health daily and remember - consistency is key! 🔑</p>
                    <p>You're building healthy habits that will last a lifetime!</p>
                </div>
            </body>
        </html>
        """
        
        return send_email(user.email, "Daily Motivation - HealthPal 💫", html_content)
        
    except Exception as e:
        print(f"Error sending motivation message: {e}")
        return False


# ==================== SCHEDULER INITIALIZATION ====================

def init_scheduler(app, db):
    """Initialize background scheduler for automated tasks"""
    scheduler = BackgroundScheduler()
    
    with app.app_context():
        # Schedule weekly reports every Sunday at 9 AM
        scheduler.add_job(
            func=lambda: send_weekly_reports_for_all_users(app, db),
            trigger=CronTrigger(day_of_week=6, hour=9, minute=0),
            id='weekly_reports',
            name='Send weekly health reports'
        )
        
        # Schedule daily reminders at 7 AM and 7 PM
        scheduler.add_job(
            func=lambda: send_daily_reminders(app, db),
            trigger=CronTrigger(hour='7,19', minute=0),
            id='daily_reminders',
            name='Send daily health reminders'
        )
        
        # Schedule motivation messages every day at 8 AM
        scheduler.add_job(
            func=lambda: send_motivation_to_all_users(app, db),
            trigger=CronTrigger(hour=8, minute=0),
            id='motivation_messages',
            name='Send daily motivation'
        )
    
    scheduler.start()
    print("Background scheduler started!")
    
    return scheduler


def send_weekly_reports_for_all_users(app, db):
    """Send weekly reports to all users on Sunday"""
    from app import User, HealthCheckIn, WeeklyHealthReport, Medication, MedicationIntake
    
    with app.app_context():
        users = User.query.all()
        for user in users:
            send_weekly_report(user.id, db, User, HealthCheckIn, WeeklyHealthReport, Medication, MedicationIntake)
            print(f"Weekly report sent to {user.email}")


def send_daily_reminders(app, db):
    """Send daily reminders to all users"""
    from app import User
    
    with app.app_context():
        users = User.query.all()
        for user in users:
            # Alternate between different reminders
            import random
            reminder_type = random.choice(['hydration', 'exercise', 'meditation', 'screen_break'])
            
            if reminder_type == 'hydration':
                send_hydration_reminder(user.id, db, User)
            elif reminder_type == 'exercise':
                send_exercise_reminder(user.id, db, User)
            elif reminder_type == 'meditation':
                send_meditation_reminder(user.id, db, User)
            elif reminder_type == 'screen_break':
                send_screen_break_reminder(user.id, db, User)
            
            if user.has_menstrual_cycle:
                send_menstrual_cycle_reminder(user.id, db, User, app.User)
            
            print(f"Daily reminder sent to {user.email}")


def send_motivation_to_all_users(app, db):
    """Send motivation messages to all users"""
    from app import User
    
    with app.app_context():
        users = User.query.all()
        for user in users:
            send_motivation_message(user.id, db, User)
            print(f"Motivation message sent to {user.email}")
