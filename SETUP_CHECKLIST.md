# HealMate - Setup Checklist

## Before Running

### 1. Google AI Setup ✓
- [ ] Visit https://makersuite.google.com/app/apikey
- [ ] Create or copy your API key
- [ ] Add to `backend/.env`: `GOOGLE_API_KEY=your-key`
- [ ] Test: Backend starts without errors

### 2. Email Setup ✓
**For Gmail:**
- [ ] Go to https://myaccount.google.com/security
- [ ] Enable 2-Factor Authentication
- [ ] Go to https://myaccount.google.com/apppasswords
- [ ] Generate App Password (select "Mail" and "Windows Computer")
- [ ] Copy the 16-character password

**Then add to `backend/.env`:**
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 3. Backend Setup ✓
```bash
cd backend
pip install -r requirements.txt
```

### 4. Frontend Setup ✓
```bash
cd frontend
npm install
```

---

## Running the App

### Start Backend
```bash
cd backend
python app.py
```
✓ Should show: `Running on http://127.0.0.1:5000`

### Start Frontend (new terminal)
```bash
cd frontend
npm start
```
✓ Should open http://localhost:3000

---

## Test Features

### ✓ Register & Login
1. Click "Register" on login page
2. Create account with email/password/name
3. Should redirect to Profile Setup

### ✓ Profile Setup
1. Fill in all fields (nickname, height, weight, BP, blood sugar, sleep hours, work times)
2. Add 1-2 medications
3. Click "Complete Setup"
4. Should redirect to Dashboard

### ✓ Dashboard
1. Should show current date/time
2. Welcome message with your nickname
3. Schedule table with water, meals, medication, sleep times
4. Should be color-coded

### ✓ Chat (AI Integration)
1. Click "Chat" in sidebar
2. Ask: "What should I eat for breakfast?"
3. Should get personalized response based on your profile
4. Check backend logs for API calls

### ✓ Email Report
1. Click "Email Report" in sidebar
2. Click "Send Weekly Report Now"
3. Should see success message
4. Check your email (may be in spam)
5. Should have formatted HTML with health metrics

### ✓ Schedule (Background Jobs)
1. Add medication with time "10:30"
2. Check backend console at 10:30
3. Should see: "Reminder for user X: [medication]..."
4. Water reminder runs every hour
5. Weekly report runs Sunday at 6 PM

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 5001
```

### CORS Errors
- Backend should have `CORS(app)` enabled ✓
- Frontend URL might need to match backend

### Chat Not Working
1. Check GOOGLE_API_KEY in `.env`
2. Test: `echo $GOOGLE_API_KEY` should show your key
3. Check backend logs for errors

### Email Not Sending
1. Verify app password (not your Gmail password)
2. Check email in SENDER_EMAIL matches
3. Check SMTP settings match your provider
4. Try sending from backend console first:
   ```python
   from app import send_email
   send_email('test@gmail.com', 'Test', 'Hello')
   ```

---

## Performance Tips

- Chat responses may take 3-5 seconds (Google AI is slow)
- Email sending happens in background (won't block UI)
- Water reminders won't show notification (just logs) - can be extended to WebSocket
- Database queries are fast (SQLite is sufficient for hackathon)

---

## Files Modified

- ✓ `backend/app.py` - Added Google AI, Email, Scheduler
- ✓ `frontend/src/App.jsx` - Added ChatPage, EmailPage components
- ✓ `frontend/src/app.css` - Added chat and email styling
- ✓ `backend/.env.example` - Updated with all required keys

---

## What's Implemented

| Feature | Status | Notes |
|---------|--------|-------|
| User Auth | ✓ Complete | Login, Register, JWT tokens |
| Profile Setup | ✓ Complete | All health fields, medications |
| Dashboard | ✓ Complete | Schedule with hourly water, meals, meds |
| Chat with AI | ✓ Complete | Google Generative AI integration |
| Weekly Email | ✓ Complete | HTML formatted with metrics |
| Reminders | ✓ Complete | Scheduled medication, water, daily, weekly |
| Daily Goals | ⏳ Partial | UI ready, backend tracking works |
| Sidebar Nav | ✓ Complete | 7 navigation options |
| Responsive | ✓ Complete | Works on mobile (480px, 768px) |

---

## Next Steps (Optional)

1. **Real-time Notifications**
   - Implement WebSocket for instant reminders
   - Show toast notifications in frontend

2. **Advanced Analytics**
   - Add charts for weekly trends
   - Calculate health scores

3. **Edit Profile**
   - Allow users to update profile after setup
   - Re-save medications

4. **Persistent Chat**
   - Load chat history on page load
   - Store conversation context

5. **Push Notifications**
   - Web push API for browser notifications
   - Mobile app notifications

---

**You're all set! 🎉 Run the commands above and test each feature.**
