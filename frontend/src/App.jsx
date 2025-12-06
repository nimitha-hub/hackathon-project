import React, { useState, useEffect } from 'react';
import './app.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// ==================== LOGIN PAGE ====================

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    console.log('Login attempt with:', { email, isRegister });
    console.log('API URL:', API_URL);
    
    try {
      let response;
      if (isRegister) {
        console.log('Registering...');
        response = await fetch(`${API_URL}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name })
        });
      } else {
        console.log('Logging in...');
        response = await fetch(`${API_URL}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
      }
      
      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
      
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userId', data.user_id);
        console.log('Login successful, calling onLogin');
        onLogin();
      } else {
        setError(data.error || (isRegister ? 'Registration failed' : 'Login failed'));
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'Network error - make sure backend is running');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="healmate-title">HealMate</h1>
        <p className="healmate-tagline">An AI-powered health companion</p>
        <h2>{isRegister ? 'Create Account' : 'Login'}</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          {isRegister && (
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          )}
          
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          
          <button type="submit" className="btn-primary">
            {isRegister ? 'Create Account' : 'Login'}
          </button>
        </form>
        
        <p>
          {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button
            type="button"
            className="link-btn"
            onClick={() => setIsRegister(!isRegister)}
          >
            {isRegister ? 'Login' : 'Register'}
          </button>
        </p>
      </div>
    </div>
  );
}

// ==================== PROFILE SETUP PAGE ====================

function ProfileSetupPage({ token, onComplete }) {
  const [profile, setProfile] = useState({
    nickname: '',
    height_cm: '',
    weight_kg: '',
    blood_type: '',
    blood_pressure_sys: '',
    blood_pressure_dia: '',
    blood_sugar_fasting: '',
    sleep_goal_hours: '',
    work_start_time: '09:00',
    work_end_time: '17:00',
    medications: []
  });
  const [newMed, setNewMed] = useState({
    name: '',
    dosage: '',
    frequency: '',
    stock_quantity: ''
  });
  const [saving, setSaving] = useState(false);

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({ ...prev, [name]: value }));
  };

  const handleAddMedication = () => {
    if (newMed.name && newMed.dosage && newMed.frequency && newMed.stock_quantity) {
      setProfile(prev => ({
        ...prev,
        medications: [...prev.medications, newMed]
      }));
      setNewMed({ name: '', dosage: '', frequency: '', stock_quantity: '' });
    }
  };

  const handleRemoveMedication = (index) => {
    setProfile(prev => ({
      ...prev,
      medications: prev.medications.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      const response = await fetch(`${API_URL}/api/user/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profile)
      });
      
      if (response.ok) {
        localStorage.setItem('profileSetup', 'true');
        onComplete();
      }
    } catch (err) {
      console.error('Profile update failed:', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="profile-setup-container">
      <div className="profile-setup-card">
        <h2>Complete Your Profile</h2>
        <p>Let's set up your health information</p>

        <form onSubmit={handleSubmit}>
          {/* Basic Info */}
          <div className="setup-section">
            <h3>Basic Information</h3>
            <input
              type="text"
              name="nickname"
              placeholder="Nickname"
              value={profile.nickname}
              onChange={handleProfileChange}
              required
            />
          </div>

          {/* Physical Measurements */}
          <div className="setup-section">
            <h3>Physical Measurements</h3>
            <div className="setup-row">
              <input
                type="number"
                name="height_cm"
                placeholder="Height (cm)"
                value={profile.height_cm}
                onChange={handleProfileChange}
              />
              <input
                type="number"
                name="weight_kg"
                placeholder="Weight (kg)"
                value={profile.weight_kg}
                onChange={handleProfileChange}
              />
            </div>
            <input
              type="text"
              name="blood_type"
              placeholder="Blood Type (e.g., O+)"
              value={profile.blood_type}
              onChange={handleProfileChange}
            />
          </div>

          {/* Health Readings */}
          <div className="setup-section">
            <h3>Health Readings</h3>
            <div className="setup-row">
              <input
                type="number"
                name="blood_pressure_sys"
                placeholder="BP Systolic"
                value={profile.blood_pressure_sys}
                onChange={handleProfileChange}
              />
              <input
                type="number"
                name="blood_pressure_dia"
                placeholder="BP Diastolic"
                value={profile.blood_pressure_dia}
                onChange={handleProfileChange}
              />
            </div>
            <input
              type="number"
              name="blood_sugar_fasting"
              placeholder="Fasting Blood Sugar (mg/dL)"
              value={profile.blood_sugar_fasting}
              onChange={handleProfileChange}
            />
          </div>

          {/* Sleep & Work */}
          <div className="setup-section">
            <h3>Sleep & Work Schedule</h3>
            <input
              type="number"
              name="sleep_goal_hours"
              placeholder="Sleep Goal (hours)"
              value={profile.sleep_goal_hours}
              onChange={handleProfileChange}
            />
            <div className="setup-row">
              <input
                type="time"
                name="work_start_time"
                value={profile.work_start_time}
                onChange={handleProfileChange}
              />
              <input
                type="time"
                name="work_end_time"
                value={profile.work_end_time}
                onChange={handleProfileChange}
              />
            </div>
          </div>

          {/* Medications */}
          <div className="setup-section">
            <h3>Medications (Optional)</h3>
            <div className="med-input-group">
              <input
                type="text"
                placeholder="Medication Name"
                value={newMed.name}
                onChange={(e) => setNewMed({...newMed, name: e.target.value})}
              />
              <input
                type="text"
                placeholder="Dosage (e.g., 500mg)"
                value={newMed.dosage}
                onChange={(e) => setNewMed({...newMed, dosage: e.target.value})}
              />
              <input
                type="text"
                placeholder="Frequency (e.g., twice daily)"
                value={newMed.frequency}
                onChange={(e) => setNewMed({...newMed, frequency: e.target.value})}
              />
              <input
                type="number"
                placeholder="Stock Quantity"
                value={newMed.stock_quantity}
                onChange={(e) => setNewMed({...newMed, stock_quantity: e.target.value})}
              />
              <button type="button" className="btn-add-med" onClick={handleAddMedication}>
                + Add
              </button>
            </div>

            {profile.medications.length > 0 && (
              <div className="med-list">
                {profile.medications.map((med, idx) => (
                  <div key={idx} className="med-item">
                    <span>{med.name} - {med.dose}, {med.frequency}</span>
                    <button 
                      type="button" 
                      onClick={() => handleRemoveMedication(idx)}
                      className="btn-remove"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button type="submit" className="btn-complete" disabled={saving}>
            {saving ? 'Saving...' : 'Complete Setup'}
          </button>
        </form>
      </div>
    </div>
  );
}

// ==================== CHAT PAGE ====================

function ChatPage({ token }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load chat history on mount
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const response = await fetch(`${API_URL}/api/chat/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const history = await response.json();
        setMessages(history);
      }
    } catch (err) {
      console.error('Failed to load chat history:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: input })
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(prev => [
          ...prev,
          { role: 'user', message: input },
          { role: 'assistant', message: data.assistant_response }
        ]);
        setInput('');
      }
    } catch (err) {
      console.error('Chat error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <h2>Chat with AI Health Assistant</h2>
      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <p>Hi! I'm your HealMate AI Assistant. Ask me anything about your health, medications, nutrition, or wellness goals.</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`chat-message ${msg.role}`}>
                <p>{msg.message}</p>
              </div>
            ))
          )}
          {loading && <div className="chat-message assistant"><p>Thinking...</p></div>}
        </div>
        <form onSubmit={handleSendMessage} className="chat-form">
          <input
            type="text"
            placeholder="Ask me about your health..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

// ==================== EMAIL PAGE ====================

function EmailPage({ token }) {
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState('');

  const handleSendEmail = async () => {
    setSending(true);
    setMessage('');
    try {
      const response = await fetch(`${API_URL}/api/send-email`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        setMessage('Weekly report sent successfully to your email!');
      } else {
        setMessage('Failed to send report. Please try again.');
      }
    } catch (err) {
      setMessage('Error sending report: ' + err.message);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="email-page">
      <h2>Email Weekly Report</h2>
      <div className="email-card">
        <h3>Send Your Weekly Health Summary</h3>
        <p>Get a comprehensive overview of your health metrics for the past week delivered to your email.</p>
        
        <div className="email-info">
          <h4>Report includes:</h4>
          <ul>
            <li>Total sleep hours</li>
            <li>Water intake</li>
            <li>Exercise minutes</li>
            <li>Meditation time</li>
            <li>Medication adherence</li>
            <li>Mood and stress levels</li>
            <li>Personalized health tips</li>
          </ul>
        </div>

        {message && <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>{message}</div>}

        <button
          className="btn-primary"
          onClick={handleSendEmail}
          disabled={sending}
          style={{ marginTop: '20px' }}
        >
          {sending ? 'Sending...' : 'Send Weekly Report Now'}
        </button>
      </div>
    </div>
  );
}

// ==================== MAIN DASHBOARD ====================

function MainDashboard({ token, onLogout }) {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [profile, setProfile] = useState(null);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [schedule, setSchedule] = useState([]);
  const [loadingError, setLoadingError] = useState(null);
  const [dailyGoals, setDailyGoals] = useState({
    medications: {},
    water: 0,
    meals: { breakfast: false, lunch: false, dinner: false }
  });

  useEffect(() => {
    fetchProfile();
    requestNotificationPermission();
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    const breakReminder = setInterval(() => {
      showNotification('🧘 Break Time!', 'Take a 30-second break from your screen to rest your eyes.');
    }, 30 * 60 * 1000); // 30 minutes
    return () => {
      clearInterval(timer);
      clearInterval(breakReminder);
    };
  }, [token]);

  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      console.log('Current notification permission:', Notification.permission);
      if (Notification.permission === 'default') {
        const permission = await Notification.requestPermission();
        console.log('Notification permission granted:', permission);
        if (permission === 'granted') {
          // Show test notification
          showNotification('🎉 Notifications Enabled!', 'You will receive health reminders every 30 minutes.');
        }
      } else if (Notification.permission === 'granted') {
        // Show test notification on dashboard load
        showNotification('👋 Welcome to HealMate!', 'Your health companion is ready to assist you.');
      }
    } else {
      console.error('This browser does not support notifications');
    }
  };

  const showNotification = (title, body) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      console.log('Showing notification:', title);
      const notification = new Notification(title, {
        body: body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        requireInteraction: false
      });
      // Auto-close after 5 seconds
      setTimeout(() => notification.close(), 5000);
    } else {
      console.log('Cannot show notification. Permission:', Notification.permission);
    }
  };

  useEffect(() => {
    if (profile) {
      generateSchedule();
    }
  }, [profile]);

  const fetchProfile = async () => {
    try {
      console.log('Fetching profile from:', `${API_URL}/api/user/profile`);
      const response = await fetch(`${API_URL}/api/user/profile`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      console.log('Profile response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Profile data:', data);
        setProfile(data);
        setLoadingError(null);
      } else {
        const errorData = await response.json();
        console.error('Profile fetch failed:', errorData);
        setLoadingError(`Failed to load profile: ${errorData.error || response.statusText}`);
      }
    } catch (err) {
      console.error('Failed to fetch profile:', err);
      setLoadingError(`Network error: ${err.message}. Make sure backend is running on ${API_URL}`);
    }
  };

  const generateSchedule = () => {
    if (!profile) return;

    const scheduleItems = [];
    const sleepHours = parseInt(profile.sleep_goal_hours) || 8;
    const wakeTime = 7; // 7 AM wake time
    const bedTime = wakeTime + 24 - sleepHours; // Calculate bedtime (e.g., 7AM + 24 - 8 = 23:00 or 11 PM)
    
    // Morning routine
    scheduleItems.push({
      time: `${wakeTime}:00`,
      activity: '☀️ Wake Up Time',
      type: 'wake'
    });

    // Breakfast
    scheduleItems.push({
      time: `${wakeTime + 1}:00`,
      activity: '🍳 Breakfast',
      type: 'food'
    });

    // Morning medications
    if (profile.medications && profile.medications.length > 0) {
      profile.medications.forEach((med, index) => {
        scheduleItems.push({
          time: '08:00',
          activity: `💊 ${med.name} (${med.dose})`,
          type: 'medication'
        });
      });
    }

    // Water reminders throughout the day
    const waterTimes = ['10:00', '14:00', '16:00', '18:00'];
    waterTimes.forEach(time => {
      scheduleItems.push({
        time: time,
        activity: '💧 Drink Water (1 glass)',
        type: 'water'
      });
    });

    // Lunch
    scheduleItems.push({
      time: '12:30',
      activity: '🍽️ Lunch',
      type: 'food'
    });

    // Afternoon break
    scheduleItems.push({
      time: '15:00',
      activity: '🧘 Take a Short Break',
      type: 'break'
    });

    // Evening medications
    if (profile.medications && profile.medications.length > 0) {
      scheduleItems.push({
        time: '20:00',
        activity: `💊 Evening Medications`,
        type: 'medication'
      });
    }

    // Dinner
    const dinnerTime = Math.min(bedTime - 2, 20); // 2 hours before bed or 8 PM
    scheduleItems.push({
      time: `${dinnerTime}:00`,
      activity: '🍽️ Dinner',
      type: 'food'
    });

    // Sleep time
    scheduleItems.push({
      time: `${bedTime % 24}:00`,
      activity: '😴 Sleep Time',
      type: 'sleep'
    });

    // Sort by time
    scheduleItems.sort((a, b) => {
      const [aHour, aMin] = a.time.split(':').map(Number);
      const [bHour, bMin] = b.time.split(':').map(Number);
      return (aHour * 60 + aMin) - (bHour * 60 + bMin);
    });

    setSchedule(scheduleItems);
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatTime12 = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  if (loadingError) {
    return (
      <div className="loading-error">
        <h2>Error Loading Profile</h2>
        <p>{loadingError}</p>
        <button onClick={fetchProfile} className="btn-primary">Retry</button>
        <button onClick={onLogout} className="btn-secondary" style={{ marginLeft: '10px' }}>Logout</button>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading your health profile...</p>
        <p style={{ fontSize: '0.9em', color: '#666', marginTop: '10px' }}>
          Connecting to {API_URL}
        </p>
      </div>
    );
  }

  return (
    <div className="main-dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>HealMate</h2>
        </div>

        <nav className="sidebar-nav">
          <button 
            className={currentPage === 'dashboard' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={currentPage === 'profile' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('profile')}
          >
            Profile
          </button>
          <button 
            className={currentPage === 'chat' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('chat')}
          >
            Chat
          </button>
          <button 
            className={currentPage === 'daily' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('daily')}
          >
            Daily Goals
          </button>
          <button 
            className={currentPage === 'weekly' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('weekly')}
          >
            Weekly Data
          </button>
          <button 
            className={currentPage === 'workout' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('workout')}
          >
            Workout Plan
          </button>
          <button 
            className={currentPage === 'email' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentPage('email')}
          >
            Email Report
          </button>
          <button className="nav-btn logout-nav" onClick={onLogout}>
            Logout
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="dashboard-content">
        {/* Dashboard Page */}
        {currentPage === 'dashboard' && (
          <div className="dashboard-page">
            <div className="time-section">
              <p className="current-date">{formatDate(currentTime)}</p>
              <p className="current-time">{formatTime12(currentTime)}</p>
            </div>

            <h1 className="welcome-msg">Welcome, {profile.nickname}!</h1>

            <div className="schedule-section">
              <h2>Today's Schedule</h2>
              <table className="schedule-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Activity</th>
                  </tr>
                </thead>
                <tbody>
                  {schedule.map((item, idx) => (
                    <tr key={idx} className={`schedule-row ${item.type}`}>
                      <td className="time-cell">{item.time}</td>
                      <td className="activity-cell">{item.activity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Profile Page */}
        {currentPage === 'profile' && (
          <div className="profile-page">
            <h2>Your Profile</h2>
            <div className="profile-card">
              <div className="profile-field">
                <label>Nickname:</label>
                <p>{profile.nickname}</p>
              </div>
              <div className="profile-field">
                <label>Height:</label>
                <p>{profile.height_cm} cm</p>
              </div>
              <div className="profile-field">
                <label>Weight:</label>
                <p>{profile.weight_kg} kg</p>
              </div>
              <div className="profile-field">
                <label>Blood Type:</label>
                <p>{profile.blood_type}</p>
              </div>
              <div className="profile-field">
                <label>Blood Pressure:</label>
                <p>{profile.blood_pressure_sys}/{profile.blood_pressure_dia}</p>
              </div>
              <div className="profile-field">
                <label>Blood Sugar:</label>
                <p>{profile.blood_sugar_fasting} mg/dL</p>
              </div>
            </div>
          </div>
        )}

        {/* Chat Page */}
        {currentPage === 'chat' && (
          <ChatPage token={token} />
        )}

        {/* Daily Goals Page */}
        {currentPage === 'daily' && (
          <div className="daily-page">
            <h2>Daily Goals Tracker</h2>
            
            {/* Medications Section */}
            <div className="goal-section">
              <h3>💊 Medications</h3>
              {profile.medications && profile.medications.length > 0 ? (
                profile.medications.map((med, index) => (
                  <div key={index} className="goal-item">
                    <label>
                      <input
                        type="checkbox"
                        checked={dailyGoals.medications[index] || false}
                        onChange={(e) => {
                          setDailyGoals({
                            ...dailyGoals,
                            medications: {
                              ...dailyGoals.medications,
                              [index]: e.target.checked
                            }
                          });
                        }}
                      />
                      <span>{med.name} - {med.dosage}</span>
                    </label>
                  </div>
                ))
              ) : (
                <p>No medications added</p>
              )}
            </div>

            {/* Water Intake Section */}
            <div className="goal-section">
              <h3>💧 Water Intake</h3>
              <div className="water-tracker">
                {[...Array(8)].map((_, i) => (
                  <button
                    key={i}
                    className={`water-glass ${i < dailyGoals.water ? 'filled' : ''}`}
                    onClick={() => setDailyGoals({ ...dailyGoals, water: i + 1 })}
                  >
                    {i < dailyGoals.water ? '💧' : '🥤'}
                  </button>
                ))}
              </div>
              <p>{dailyGoals.water} / 8 glasses</p>
            </div>

            {/* Meals Section */}
            <div className="goal-section">
              <h3>🍽️ Meals</h3>
              <div className="goal-item">
                <label>
                  <input
                    type="checkbox"
                    checked={dailyGoals.meals.breakfast}
                    onChange={(e) => setDailyGoals({
                      ...dailyGoals,
                      meals: { ...dailyGoals.meals, breakfast: e.target.checked }
                    })}
                  />
                  <span>Breakfast</span>
                </label>
              </div>
              <div className="goal-item">
                <label>
                  <input
                    type="checkbox"
                    checked={dailyGoals.meals.lunch}
                    onChange={(e) => setDailyGoals({
                      ...dailyGoals,
                      meals: { ...dailyGoals.meals, lunch: e.target.checked }
                    })}
                  />
                  <span>Lunch</span>
                </label>
              </div>
              <div className="goal-item">
                <label>
                  <input
                    type="checkbox"
                    checked={dailyGoals.meals.dinner}
                    onChange={(e) => setDailyGoals({
                      ...dailyGoals,
                      meals: { ...dailyGoals.meals, dinner: e.target.checked }
                    })}
                  />
                  <span>Dinner</span>
                </label>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="progress-section">
              <h3>Overall Progress</h3>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ 
                    width: `${(
                      (Object.values(dailyGoals.medications).filter(Boolean).length / Math.max(profile.medications?.length || 1, 1)) * 33 +
                      (dailyGoals.water / 8) * 33 +
                      (Object.values(dailyGoals.meals).filter(Boolean).length / 3) * 34
                    ).toFixed(0)}%`
                  }}
                ></div>
              </div>
              <p className="progress-text">
                {(
                  (Object.values(dailyGoals.medications).filter(Boolean).length / Math.max(profile.medications?.length || 1, 1)) * 33 +
                  (dailyGoals.water / 8) * 33 +
                  (Object.values(dailyGoals.meals).filter(Boolean).length / 3) * 34
                ).toFixed(0)}% Complete
              </p>
            </div>
          </div>
        )}

        {/* Weekly Data Page */}
        {currentPage === 'weekly' && (
          <div className="weekly-page">
            <h2>Weekly Data</h2>
            <p>Weekly analytics coming soon...</p>
          </div>
        )}

        {/* Workout Page */}
        {currentPage === 'workout' && (
          <div className="workout-page">
            <h2>AI Workout Plan</h2>
            <p>Personalized workout plan coming soon...</p>
          </div>
        )}

        {/* Email Report Page */}
        {currentPage === 'email' && (
          <EmailPage token={token} />
        )}
      </main>
    </div>
  );
}

// ==================== MAIN APP ====================

export default function App() {
  // Debug logging for localStorage state
  console.log('App mount:', {
    token: localStorage.getItem('token'),
    profileSetup: localStorage.getItem('profileSetup')
  });
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [profileSetup, setProfileSetup] = useState(localStorage.getItem('profileSetup') === 'true');

  const handleLogin = () => {
    const newToken = localStorage.getItem('token');
    setToken(newToken);
    setIsLoggedIn(true);
    // Reset profileSetup on login to force profile setup for new users
    const setup = localStorage.getItem('profileSetup') === 'true';
    setProfileSetup(setup);
    console.log('Login:', { token: newToken, profileSetup: setup });
  };

  const handleProfileComplete = () => {
    // Only set profileSetup after successful profile update
    localStorage.setItem('profileSetup', 'true');
    setProfileSetup(true);
    console.log('Profile setup complete, redirecting to dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('profileSetup');
    setIsLoggedIn(false);
    setToken(null);
    setProfileSetup(false);
    console.log('Logout: cleared localStorage');
  };

  if (!isLoggedIn) {
    console.log('Rendering LoginPage');
    return <LoginPage onLogin={handleLogin} />;
  }

  if (!profileSetup) {
    console.log('Rendering ProfileSetupPage');
    return <ProfileSetupPage token={token} onComplete={handleProfileComplete} />;
  }

  console.log('Rendering MainDashboard');
  return <MainDashboard token={token} onLogout={handleLogout} />;
}

