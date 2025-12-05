# HealMate Architecture & Data Flow

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Browser)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS/WS
                             │
        ┌────────────────────▼────────────────────┐
        │                                         │
        │      FRONTEND (React + CSS)            │
        │                                         │
        │  ┌──────────────────────────────────┐ │
        │  │ Pages                            │ │
        │  │ ├── LoginPage                    │ │
        │  │ ├── ProfileSetupPage             │ │
        │  │ ├── MainDashboard                │ │
        │  │ │   ├── Dashboard View           │ │
        │  │ │   ├── Profile View             │ │
        │  │ │   ├── ChatPage ✨              │ │
        │  │ │   ├── Daily Goals              │ │
        │  │ │   ├── Weekly Data              │ │
        │  │ │   ├── Workout Plan             │ │
        │  │ │   └── EmailPage ✨             │ │
        │  └──────────────────────────────────┘ │
        │                                         │
        │  Styling: Gradients, Colors, Fonts    │
        │  State: useState, useEffect hooks      │
        │  Auth: JWT tokens in localStorage      │
        │                                         │
        └────────────────────┬────────────────────┘
                             │ REST API + JWT
                             │ (http://localhost:5000)
                             │
        ┌────────────────────▼────────────────────────────────────┐
        │                                                          │
        │      BACKEND (Flask + SQLAlchemy)                      │
        │                                                          │
        │  ┌────────────────────────────────────────────────┐   │
        │  │ API Routes                                     │   │
        │  │ ├── /api/auth/* (Login, Register)             │   │
        │  │ ├── /api/user/* (Profile GET/PUT)             │   │
        │  │ ├── /api/medications/* (Get, Add, Update)     │   │
        │  │ ├── /api/chat ✨ (Send message, history)      │   │
        │  │ ├── /api/send-email ✨ (Trigger report)       │   │
        │  │ ├── /api/health-checkin/* (Check-ins)         │   │
        │  │ ├── /api/daily-goals/* (Goals, progress)      │   │
        │  │ └── /health (Health check)                    │   │
        │  └────────────────────────────────────────────────┘   │
        │                                                          │
        │  ┌────────────────────────────────────────────────┐   │
        │  │ Core Functions ✨ NEW                          │   │
        │  │ ├── generate_ai_response()                     │   │
        │  │ ├── send_email()                               │   │
        │  │ ├── generate_weekly_report()                   │   │
        │  │ └── schedule_* (Scheduler functions)           │   │
        │  └────────────────────────────────────────────────┘   │
        │                                                          │
        │  ┌────────────────────────────────────────────────┐   │
        │  │ Authentication                                 │   │
        │  │ ├── JWT Secret Key                             │   │
        │  │ ├── @jwt_required() decorator                  │   │
        │  │ └── get_jwt_identity()                         │   │
        │  └────────────────────────────────────────────────┘   │
        │                                                          │
        │  ┌────────────────────────────────────────────────┐   │
        │  │ Background Services ✨ NEW                     │   │
        │  │ ├── APScheduler                                │   │
        │  │ │   ├── Medication reminders (cron)            │   │
        │  │ │   ├── Water reminders (1h interval)          │   │
        │  │ │   ├── Daily summary (cron 21:00)             │   │
        │  │ │   └── Weekly reports (cron Sun 18:00)        │   │
        │  │ ├── Google Generative AI                       │   │
        │  │ └── SMTP Email Service                         │   │
        │  └────────────────────────────────────────────────┘   │
        │                                                          │
        └────────────────────┬─────────────────────────────────────┘
                             │
        ┌────────────────────┼──────────────────────────┐
        │                    │                          │
        │                    │                          │
┌───────▼──────────┐ ┌──────▼─────────────┐   ┌──────▼─────────┐
│  SQLite          │ │ Google Generative  │   │  Gmail SMTP    │
│  Database        │ │ AI API             │   │  Email Service │
│                  │ │                    │   │                │
│ ┌──────────────┐ │ │ model: gemini-pro  │   │ server: SMTP   │
│ │ users        │ │ │ key: GOOGLE_API..  │   │ auth: app-pass │
│ ├──────────────┤ │ │                    │   │                │
│ │ medications  │ │ │ Features:          │   │ Sends:         │
│ ├──────────────┤ │ │ • Context-aware    │   │ • HTML emails  │
│ │ health_      │ │ │ • Profile-based    │   │ • Weekly       │
│ │ checkins     │ │ │ • Personalized     │   │   reports      │
│ ├──────────────┤ │ │ • Multi-turn chat  │   │ • Metrics      │
│ │ chat_        │ │ │                    │   │                │
│ │ messages     │ │ │ Latency: 3-5s      │   │ Latency: 1-2s  │
│ ├──────────────┤ │ │                    │   │                │
│ │ daily_goals  │ │ │ Cost: Free tier    │   │ Cost: Free     │
│ ├──────────────┤ │ │                    │   │                │
│ │ weekly_      │ │ └────────────────────┘   └────────────────┘
│ │ reports      │ │
│ ├──────────────┤ │
│ └──────────────┘ │
│                  │
│ Relationships:   │
│ • User 1→∞ Med  │
│ • User 1→∞ Chat │
│ • Med 1→∞ Intake│
│ • User 1→∞ Goal │
│ • User 1→∞ Rept │
│                  │
└──────────────────┘
```

---

## Data Flow Diagrams

### 1. Chat Feature Flow ✨

```
User Types Message
       ↓
┌─────────────────────────────────┐
│ Frontend: ChatPage Component     │
│ • setState({ input: "..." })    │
│ • handleSendMessage()           │
└────────────┬────────────────────┘
             │
             ↓
       Send to Backend
    POST /api/chat
    Headers: Authorization: Bearer {token}
    Body: { message: "user question" }
             │
             ↓
┌─────────────────────────────────┐
│ Backend: chat() endpoint         │
│ • Get user_id from JWT          │
│ • Load User profile             │
│ • Save user message to DB       │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ AI: generate_ai_response()      │
│ • Build user context:           │
│   - Age, height, weight         │
│   - Blood pressure, sugar       │
│   - Medications list            │
│   - Job, stress level           │
│   - Dietary restrictions        │
│ • Call Google Generative AI     │
│ • API Request:                  │
│   Model: gemini-pro             │
│   Prompt: context + message     │
│ • Wait 3-5 seconds for response │
│ • Extract text from response    │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Backend: Save & Return          │
│ • Save AI response to ChatMsg   │
│ • Return to frontend:           │
│   { user_message, response }    │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│ Frontend: Display Response      │
│ • Add to messages array         │
│ • Show in chat bubble           │
│ • User sees personalized advice │
│ • Can ask follow-up question    │
└─────────────────────────────────┘
```

### 2. Email Report Flow ✨

```
User Clicks "Send Weekly Report"
       ↓
┌─────────────────────────────────┐
│ Frontend: EmailPage Component   │
│ • handleSendEmail()             │
│ • Disabled button (sending...) │
└────────────┬────────────────────┘
             │
             ↓
       Send to Backend
    POST /api/send-email
    Headers: Authorization: Bearer {token}
             │
             ↓
┌─────────────────────────────────┐
│ Backend: send_email() endpoint  │
│ • Get user_id from JWT          │
│ • Call generate_weekly_report() │
└────────────┬────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│ Report Generation               │
│ • Calculate week dates          │
│ • Query health_checkins (7 days)│
│ • Sum metrics:                  │
│   - total_sleep_hours           │
│   - total_water_liters          │
│   - total_exercise_minutes      │
│   - medication_adherence_%      │
│   - average_mood                │
│   - average_stress              │
│ • Create WeeklyHealthReport row │
│ • Generate HTML email body:     │
│   - User name, date range       │
│   - All metrics in styled cards │
│   - Health tips                 │
│   - Branded footer              │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│ Email Sending                   │
│ • Build MIME message            │
│ • Add text + HTML versions      │
│ • Connect to Gmail SMTP:        │
│   - server: smtp.gmail.com      │
│   - port: 587                   │
│   - auth: app-specific password │
│ • Send to user.email            │
│ • Update report_sent = True     │
│ • Set sent_at timestamp         │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│ Frontend: Show Success Message  │
│ • Display: "Email sent!"        │
│ • Clear error state             │
│ • Re-enable button              │
│                                 │
│ Backend: Return Success         │
│ { message: "...sent success" }  │
└──────────────────────────────────┘
     ↓
User checks email inbox (1-2 minutes)
     ↓
Beautiful HTML email received!
```

### 3. Scheduler Jobs Flow ✨

```
App Startup
    ↓
┌──────────────────────────────────┐
│ @app.before_request              │
│ init_schedulers()                │
│ • Check if already initialized   │
│ • Call all schedule functions:   │
│   1. schedule_medication_rmnds() │
│   2. schedule_water_reminders()  │
│   3. schedule_daily_report()     │
│   4. schedule_weekly_reports()   │
└────────────┬─────────────────────┘
             │
             ├──────────────────────┬──────────────────┬────────────────┐
             │                      │                  │                │
             ▼                      ▼                  ▼                ▼
    ┌─────────────────┐   ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Medication      │   │ Water Reminders │  │ Daily Report │  │ Weekly       │
    │ Reminders       │   │                 │  │              │  │ Reports      │
    ├─────────────────┤   ├─────────────────┤  ├──────────────┤  ├──────────────┤
    │ • For each user │   │ • For each user │  │ • Cron job   │  │ • Cron job   │
    │ • For each med  │   │ • 1-hour        │  │ • At 21:00   │  │ • Sun 18:00  │
    │ • Parse times   │   │   interval      │  │   (9 PM)     │  │ • Calls      │
    │   from DB       │   │ • Every hour    │  │ • Call       │  │   generate_  │
    │ • Create cron   │   │   during day    │  │   reminder() │  │   weekly_    │
    │   jobs for      │   │ • Log: "drink   │  │ • Log:       │  │   report()   │
    │   each time     │   │   water"        │  │   "daily     │  │ • Sends      │
    │   (e.g. 8:00)   │   │                 │  │   summary"   │  │   email      │
    │ • Runs daily    │   │                 │  │              │  │              │
    │ • Log: "take    │   │                 │  │              │  │              │
    │   med X"        │   │                 │  │              │  │              │
    └─────────────────┘   └─────────────────┘  └──────────────┘  └──────────────┘
             │                      │                  │                │
             │    ┌────────────────┼──────────────────┼────────────────┤
             │    │                │                  │                │
             ▼    ▼                ▼                  ▼                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │ APScheduler Background Process                                  │
    │                                                                  │
    │ • Jobs run on schedule (cron or interval)                      │
    │ • Don't block API requests                                     │
    │ • Run in Flask app context                                     │
    │ • Logging to console for debugging                             │
    │ • Survives until app shutdown                                  │
    │                                                                  │
    │ Example activity (from console):                               │
    │ [09:00:00] Reminder: Take Medication: Lisinopril               │
    │ [10:00:00] Reminder: Drink water! Stay hydrated                │
    │ [12:30:00] Reminder: Lunch time - eat healthily                │
    │ [21:00:00] Reminder: Daily summary...                          │
    │ [Sun 18:00] Generating weekly report for user_123...           │
    │ [Sun 18:02] Email sent to user@example.com                     │
    └──────────────────────────────────────────────────────────────────┘
```

---

## Request/Response Flow

### Chat Request/Response

**Request:**
```json
POST /api/chat
Headers: {
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs...",
  "Content-Type": "application/json"
}
Body: {
  "message": "I have high blood pressure, what should I eat?"
}
```

**Response (3-5 sec later):**
```json
{
  "user_message": "I have high blood pressure, what should I eat?",
  "assistant_response": "Based on your profile showing blood pressure of 138/88, I recommend a DASH diet with less sodium. You should eat more leafy greens, whole grains, and lean proteins. Avoid processed foods and reduce salt intake. Your current medications like Lisinopril work best with this diet...",
  "timestamp": "2025-12-05T14:30:45.123Z"
}
```

### Email Request/Response

**Request:**
```json
POST /api/send-email
Headers: {
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (1-2 sec):**
```json
{
  "message": "Weekly report email sent successfully"
}
```

**Email Received (1-5 min):**
```
To: user@example.com
Subject: HealMate Weekly Report - Dec 1-7, 2025

[HTML Content]
HealMate Weekly Health Report

Hi Nimitha,

Here's your health summary for the week of December 1-7, 2025:

Weekly Metrics
💤 Sleep: 52.5 hours (Goal: 56h)
💧 Water: 42.0 liters (Goal: 56L)
🏃 Exercise: 180 minutes (Goal: 210m)
🧘 Meditation: 70 minutes
💊 Medication Adherence: 95%
😊 Average Mood: Happy
😰 Average Stress: 4.2/10

Tips for Next Week
• Keep up your sleep schedule consistency
• Increase water intake by 2-3 glasses daily
• Continue with meditation - it's working!
• Don't miss your medications - set phone reminders
...
```

---

## Database Schema (Relevant Tables)

### chat_messages
```
id (PK) | user_id (FK) | role | message | created_at
--------|--------------|------|---------|------------
1       | 5            | user | "Hi"    | 2025-12-05...
2       | 5            | asst | "Hello" | 2025-12-05...
```

### weekly_reports
```
id | user_id | week_start | week_end | sleep_hrs | water | meds_% | avg_mood | sent
---|---------|-----------|----------|-----------|-------|--------|----------|-----
1  | 5       | 2025-11-30 | 2025-12-06 | 52.5 | 42.0 | 95 | happy | true
```

---

## Environment Variables

```env
# Google AI
GOOGLE_API_KEY=AIzaSyDhX1234567890ABCDEFGH...

# Email
SENDER_EMAIL=healmate@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop  (16-char app password)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# JWT
JWT_SECRET_KEY=super-secret-key-change-in-production
```

---

## Scheduler Timeline Example

```
Monday
  08:00 → Take Lisinopril (medication reminder)
  09:00 → Drink water!
  10:00 → Drink water!
  12:00 → Drink water!
  12:30 → Lunch time
  13:00 → Drink water!
  ... (hourly water until sleep time)
  21:00 → Daily summary reminder
  22:00 → Sleep time

Tuesday - Friday (similar pattern)

Saturday (similar pattern)

Sunday
  18:00 → Generate weekly report
  18:02 → Send email to user@example.com
  19:00 → Drink water!
  21:00 → Daily summary

Next Week
  Monday 08:00 → Medication reminder again...
  (Pattern repeats)
```

---

This completes the HealMate architecture documentation! 🎉
