# HealthPal - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

---

## Backend Setup (Terminal 1)

### Step 1: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your settings
# Minimum required:
# JWT_SECRET_KEY=any-random-string
```

### Step 3: Run Backend
```bash
python app.py
```

**Expected Output:**
```
WARNING in flask_sqlalchemy: SQLAlchemy is configured to use SQLite...
 * Running on http://127.0.0.1:5000
```

Backend is ready at `http://localhost:5000`

---

## Frontend Setup (Terminal 2)

### Step 1: Navigate to Frontend
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Start Development Server
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view healthpal-frontend in the browser.
  Local: http://localhost:3000
```

Frontend opens at `http://localhost:3000`

---

## 🧪 Testing the Application

### 1. Register a New Account
- Go to `http://localhost:3000`
- Click "Register"
- Fill in: Email, Password, Name
- Click "Create Account"

### 2. Set Up Health Profile
- Fill in all health parameters
- **Important**: Set at least these fields:
  - Age
  - Height & Weight
  - Sleep Goal (hours)
  - Exercise Goal (minutes)
- Click "Complete Profile Setup"

### 3. Daily Health Check-in
- Click "Daily Check-in" tab
- Fill in mood, sleep hours, water intake, etc.
- Click "Save Check-in"

### 4. View Dashboard
- Click "Dashboard" tab
- See daily goals and progress
- Check completion percentage

### 5. Add Medications
- Click "Medications" tab
- Click "+ Add Medication"
- Add a test medication (e.g., Aspirin)
- Click "Log Intake" to test

### 6. Chat with AI
- Click "Chat" tab
- Ask questions like:
  - "How's my sleep?"
  - "Should I exercise today?"
  - "Help with stress"
- See AI responses

---

## 📧 Email Configuration (Optional)

To enable weekly reports and reminders:

### Gmail Setup
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Generate an app password
3. Update `.env`:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
```

### Other Providers
- **Outlook**: `smtp.office365.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **SendGrid**: `smtp.sendgrid.net:587`

---

## 🔄 API Testing with Curl

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","name":"John Doe"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

**Save the token from response for next requests**

### Get User Profile
```bash
curl -X GET http://localhost:5000/api/user/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Check-in
```bash
curl -X POST http://localhost:5000/api/health-checkin \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "mood":"happy",
    "stress_level":5,
    "sleep_hours":8,
    "water_intake_liters":7,
    "exercise_minutes":30,
    "meditation_minutes":10
  }'
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Clear database and restart
rm backend/health_assistant.db
python app.py
```

### Port already in use
```bash
# Change port in app.py (last line)
app.run(debug=True, port=5001)  # Changed from 5000
```

### Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check CORS is enabled in `app.py`
- Verify API URLs in `app.jsx` match your backend

### Dependencies issues
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Project Structure

```
HealthPal/
├── backend/
│   ├── app.py                 # Main Flask app + API endpoints
│   ├── utilities.py           # Email, scheduling, notifications
│   ├── advanced_features.py   # Nutrition, insights, schedule generation
│   ├── requirements.txt       # Python packages
│   ├── .env.example          # Environment template
│   └── health_assistant.db   # SQLite database (auto-created)
│
├── frontend/
│   ├── app.jsx               # React components
│   ├── app.css               # Styling
│   ├── package.json          # NPM packages
│   └── node_modules/         # Dependencies (auto-created)
│
└── README.md
```

---

## 🎯 Key Features to Demo

### 1. User Registration & Profile
- Show authentication flow
- Explain all profile fields
- Demonstrate profile edit

### 2. Daily Tracking
- Log mood, sleep, water, exercise
- Show progress bar updates
- Display completion percentage

### 3. Medication Management
- Add medications
- Log medication intake
- Show refill warnings

### 4. Dashboard
- Display daily goals
- Show progress metrics
- Highlight achievements

### 5. AI Chat
- Ask health questions
- Get personalized advice
- Show conversation history

### 6. Weekly Reports (Backend Feature)
- Explain automated Sunday emails
- Show report format
- Demonstrate weekly statistics

---

## 📈 Next Steps for Enhancement

### Immediate (1-2 hours)
- [ ] Integrate Google Generative AI for better chat responses
- [ ] Add nutrition suggestions API endpoint
- [ ] Implement meditation video recommendations

### Short Term (3-5 hours)
- [ ] Add fitness tracker integration (Fitbit API)
- [ ] Implement progress charts and analytics
- [ ] Add social features (friend challenges)

### Medium Term (6-10 hours)
- [ ] Mobile app (React Native)
- [ ] Push notifications
- [ ] Video consultation booking
- [ ] Advanced health predictions

---

## 💡 Demo Talking Points

1. **Problem Solved**: Personalized AI health assistant that tracks all health metrics
2. **Unique Value**: Daily schedule generation + medication tracking + motivational support
3. **Technology**: Full-stack (React, Flask, SQLAlchemy, APScheduler)
4. **Scalability**: Database models ready for growth
5. **User Retention**: Gamification with daily goals and achievements
6. **Business Model**: Premium features for advanced analytics

---

## ✅ Hackathon Submission Checklist

- [x] Backend API fully functional
- [x] Frontend UI complete
- [x] User authentication
- [x] Daily tracking
- [x] Medication management
- [x] AI chatbot
- [x] Email notifications setup
- [x] Database models
- [x] API documentation
- [x] README

---

## 📱 Quick Demo Script (2-3 minutes)

```
1. Open http://localhost:3000
2. Register: testuser@example.com / password
3. Fill profile → Complete
4. Dashboard tab → Show goals
5. Daily Check-in → Log data
6. Click "Dashboard" → Show progress
7. Medications → Add & Log
8. Chat → Ask "How's my sleep?"
9. Profile → Show all tracked data
10. Explain weekly email feature
```

---

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **React**: https://react.dev/
- **APScheduler**: https://apscheduler.readthedocs.io/

---

## 📞 Support & Debugging

### Enable Debug Logging
```python
# In app.py, before app.run()
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Database
```bash
# View SQLite database
sqlite3 backend/health_assistant.db

# See all tables
.tables

# View user data
SELECT * FROM users;
```

### Frontend Console
- Press `F12` to open dev tools
- Go to Console tab
- Watch for API errors
- Check Network tab for requests

---

**Good luck with your hackathon! 🚀**

Remember: Focus on demonstrating core features that solve the health tracking problem effectively!
