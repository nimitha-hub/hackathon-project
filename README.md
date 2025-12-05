# HealthPal - AI Health Assistant

Your 24/7 intelligent health companion that helps you maintain a healthy lifestyle with personalized daily schedules, medication tracking, wellness reminders, and AI-powered health guidance.

## 🌟 Features

### Core Features
- **User Profile Management**: Set up comprehensive health profile with personal info, measurements, lifestyle, and preferences
- **Daily Health Tracking**: Log mood, medications, water intake, exercise, sleep, meditation daily
- **Daily Goals Dashboard**: AI-generated daily health goals with progress tracking
- **Medication Management**: Track medications, set refill reminders, log medication intake
- **AI Chat Assistant**: 24/7 health companion for wellness guidance and support
- **Weekly Health Reports**: Sunday reports with motivation on email

### Smart Reminders
- 💧 Water intake reminders
- 💊 Medication reminders with stock tracking
- 🏃 Exercise reminders
- 🧘 Meditation reminders
- 👁️ Screen break reminders
- 🩸 Menstrual cycle tracking and reminders
- 💪 Daily motivation messages

### Health Tracking
- Sleep monitoring with goals
- Water hydration tracking
- Exercise tracking with time logging
- Meditation progress
- Mood tracking
- Medication adherence tracking
- Blood pressure and blood sugar monitoring

## 🏗️ Project Structure

```
Hackathon/
├── backend/
│   ├── app.py                 # Main Flask application & database models
│   ├── utilities.py           # Scheduling, email, notifications
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── app.jsx               # React application with all components
│   ├── app.css               # Comprehensive styling
│   └── package.json          # Frontend dependencies
└── README.md
```

## 🚀 Quick Start

### Backend Setup

1. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   
   Configure these variables:
   - `JWT_SECRET_KEY`: Your secret key for JWT tokens
   - `SMTP_SERVER`, `SMTP_PORT`, `SENDER_EMAIL`, `SENDER_PASSWORD`: Email configuration

3. **Run the Flask server**
   ```bash
   python app.py
   ```
   
   Backend will start at `http://localhost:5000`

### Frontend Setup

1. **Create React app** (if not using existing)
   ```bash
   npx create-react-app frontend
   cd frontend
   ```

2. **Copy frontend files**
   - Replace `src/App.jsx` with the provided `app.jsx`
   - Replace `src/App.css` with the provided `app.css`

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Start the React development server**
   ```bash
   npm start
   ```
   
   Frontend will open at `http://localhost:3000`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### User Profile
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

### Medications
- `GET /api/medications` - Get all medications
- `POST /api/medications` - Add new medication
- `PUT /api/medications/<id>` - Update medication
- `POST /api/medications/<id>/intake` - Log medication intake

### Health Check-ins
- `POST /api/health-checkin` - Create daily check-in
- `GET /api/health-checkin/today` - Get today's check-in
- `PUT /api/health-checkin/<id>` - Update check-in

### Daily Goals
- `GET /api/daily-goals/today` - Get today's goals
- `PUT /api/daily-goals/<id>/progress` - Update goal progress

### Chat
- `POST /api/chat` - Send message to AI assistant
- `GET /api/chat/history` - Get chat message history

## 🎯 User Flow

### First Time Setup
1. Register account
2. Complete health profile setup
3. View dashboard

### Daily Workflow
1. Log in
2. Complete daily health check-in
3. View and track daily goals
4. Log medication intake
5. Chat with AI assistant for guidance
6. Track progress in dashboard

### Weekly
- Automatically receive weekly health report on Sunday
- Review achievements and get motivated
- Update health profile if needed

## 🔐 Security Features

- JWT-based authentication
- Password hashing (implement bcrypt in production)
- CORS protection
- Protected API endpoints

## 💻 Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database
- **Flask-JWT-Extended**: JWT authentication
- **APScheduler**: Scheduled tasks
- **Flask-CORS**: CORS handling

### Frontend
- **React**: UI framework
- **CSS3**: Styling with gradients and animations
- **Fetch API**: HTTP requests

### Database
- **SQLite**: Development database

## 📧 Email Configuration

To enable email notifications:

1. **Gmail Setup**
   - Enable 2-factor authentication
   - Generate App Password
   - Add to `.env`:
     ```
     SENDER_EMAIL=your-email@gmail.com
     SENDER_PASSWORD=your-16-char-app-password
     ```

2. **Other Email Providers**
   - Update `SMTP_SERVER` and `SMTP_PORT` in `.env`

## 🤖 AI Integration

Currently has placeholder AI responses. To integrate with Google Generative AI:

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GOOGLE_API_KEY=your-key`
3. Uncomment Google AI integration in `utilities.py`

## 📱 Responsive Design

- Mobile-friendly interface
- Tablet optimization
- Desktop view
- Touch-friendly buttons and inputs

## 🔄 Automated Reminders

The system automatically sends:
- **Daily (7 AM & 7 PM)**: Health reminders (hydration, exercise, meditation, screen breaks)
- **Weekly (Sunday 9 AM)**: Health report with weekly stats
- **Daily (8 AM)**: Motivational messages

## 💾 Database Schema

### Key Tables
- **users**: User profiles and preferences
- **medications**: Medication tracking
- **medication_intakes**: Logs of medication taken
- **health_checkins**: Daily health data
- **daily_goals**: Daily targets and progress
- **chat_messages**: Chat history
- **weekly_health_reports**: Weekly summaries

## 🛠️ Development Tips

### Adding New Features

1. **Backend**: Add endpoint in `app.py`
2. **Database**: Add model to `app.py`
3. **Frontend**: Add component to `app.jsx`
4. **Styling**: Update `app.css`

### Testing Endpoints

Use Postman or curl:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```

## 📊 Future Enhancements

- [ ] Nutrition suggestions based on health data
- [ ] Integration with fitness trackers (Fitbit, Apple Health)
- [ ] Video consultation with doctors
- [ ] Community challenges
- [ ] Predictive health alerts
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and trends
- [ ] Social features and achievements

## 📄 License

This is a hackathon project. Feel free to use and modify for your needs.

## 👥 Team

Built with ❤️ for the hackathon Aventron by Team Cyber Clan


For issues and questions, open an issue in the repository.

---

**Stay Healthy, Stay Happy! 🏥💪**
