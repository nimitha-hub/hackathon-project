# Backend Integration Guide

This document explains all the new integrations added to the HealMate backend.

## 1. Google Generative AI Integration

### Setup
1. Get your Google API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`:
```
GOOGLE_API_KEY=your-key-here
```

### Features
- Smart AI chat assistant that understands user health profile
- Personalized health advice based on medications, blood pressure, age, etc.
- Contextual responses that reference user's specific health data

### API Endpoint
```
POST /api/chat
Authorization: Bearer {token}
Body: { "message": "user question" }

Response: {
  "user_message": "...",
  "assistant_response": "AI generated response",
  "timestamp": "2025-12-05T..."
}
```

---

## 2. Email Notifications & Weekly Reports

### Setup
1. For Gmail (recommended):
   - Enable 2-Factor Authentication: https://myaccount.google.com/security
   - Generate App Password: https://myaccount.google.com/apppasswords
   - Add to `.env`:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

2. For other email providers:
   - Update SMTP_SERVER and SMTP_PORT accordingly
   - Use app-specific password if available

### Features
- Automatic weekly health reports sent every Sunday at 6 PM
- Includes: sleep hours, water intake, exercise, meditation, medication adherence, mood, stress levels
- Beautiful HTML-formatted emails with health metrics and personalized tips
- Manual trigger via frontend button

### API Endpoint
```
POST /api/send-email
Authorization: Bearer {token}

Response: { "message": "Weekly report email sent successfully" }
```

### Database
- `WeeklyHealthReport` model stores all generated reports
- Tracks: week_start_date, week_end_date, metrics, send status

---

## 3. Background Scheduler (APScheduler)

### Features

#### Medication Reminders
- Scheduled based on user's medication times (stored as JSON in db)
- Runs at specified times daily
- Can be extended to send push notifications

#### Water Reminders
- Hourly reminders during waking hours
- Runs every hour automatically

#### Daily Summary
- Sent at 9 PM daily
- Reminds users to check their progress

#### Weekly Reports
- Automatically generated every Sunday at 6 PM
- Aggregates week's health data
- Sends email to user

### How It Works
1. Scheduler initializes on app startup (`init_schedulers()`)
2. All jobs are created with unique IDs per user
3. Jobs run in background, don't block API requests
4. Can be viewed/managed via APScheduler dashboard (optional)

### Configuration
Edit the scheduled times in `app.py`:
```python
schedule_medication_reminders()  # Based on medication times
schedule_water_reminders()       # Every 1 hour
schedule_daily_report()          # At 21:00 (9 PM)
schedule_weekly_reports()        # Sunday at 18:00 (6 PM)
```

---

## Database Models

### Enhanced Models

#### WeeklyHealthReport
```python
{
  id: integer,
  user_id: integer,
  week_start_date: date,
  week_end_date: date,
  total_sleep_hours: float,
  total_water_liters: float,
  medication_adherence_percent: float,
  exercise_minutes: integer,
  meditation_minutes: integer,
  average_mood: string,
  report_sent: boolean,
  sent_at: datetime,
  created_at: datetime
}
```

---

## How to Run

### 1. Install Requirements
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your keys and email settings
```

### 3. Run Backend
```bash
python app.py
```

### 4. Run Frontend
```bash
cd ../frontend
npm install
npm start
```

---

## Testing

### Test Google AI Chat
1. Login to app
2. Go to Chat page
3. Ask a health question
4. Response should be personalized based on your profile

### Test Email
1. Go to Email Report page
2. Click "Send Weekly Report Now"
3. Check email for formatted HTML report

### Test Scheduler
1. Add a medication with time "HH:MM"
2. Watch backend logs for scheduled reminders
3. Weekly reports will send Sunday at 6 PM

---

## Troubleshooting

### Chat returns error
- Verify GOOGLE_API_KEY is set in `.env`
- Check internet connection
- Ensure key has Generative AI access

### Email not sending
- Verify SENDER_EMAIL and SENDER_PASSWORD are correct
- For Gmail: Ensure App Password is used (not regular password)
- Check SMTP_SERVER and SMTP_PORT match your email provider
- Enable "Less secure app access" if not using Gmail App Password

### Scheduler not running
- Check backend logs for errors
- Verify APScheduler is installed: `pip list | grep APScheduler`
- Ensure app is running (scheduler needs Flask context)

---

## Architecture

### Flow Diagram

```
Frontend (React)
    ↓
Flask Backend
    ├── Auth & User Management
    ├── Google AI Chat
    ├── Email Service
    └── Scheduler (Background Jobs)
        ├── Medication Reminders
        ├── Water Reminders
        └── Weekly Reports
    ↓
SQLite Database
    ├── Users
    ├── Medications
    ├── Health Check-ins
    ├── Chat Messages
    └── Weekly Reports
```

---

## API Summary

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/auth/login` | POST | No | User login |
| `/api/auth/register` | POST | No | User registration |
| `/api/user/profile` | GET | Yes | Get user profile |
| `/api/user/profile` | PUT | Yes | Update user profile |
| `/api/medications` | GET | Yes | Get medications |
| `/api/medications` | POST | Yes | Add medication |
| `/api/chat` | POST | Yes | Send chat message |
| `/api/chat/history` | GET | Yes | Get chat history |
| `/api/send-email` | POST | Yes | Send weekly report |
| `/api/health-checkin` | POST | Yes | Create daily check-in |
| `/api/daily-goals/today` | GET | Yes | Get today's goals |

---

## Future Enhancements

1. **WebSocket Integration**: Real-time reminders instead of polling
2. **Push Notifications**: Mobile app push notifications
3. **Advanced Analytics**: Charts and trend analysis
4. **AI Insights**: Weekly AI-generated health insights
5. **Smart Scheduling**: ML-based optimal reminder timing
6. **Wearable Integration**: Sync with Fitbit, Apple Watch, etc.
