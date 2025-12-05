import React, { useState, useEffect } from 'react';
import './app.css';

// ==================== CONTEXT & AUTHENTICATION ====================

const AuthContext = React.createContext();

const useAuth = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userId, setUserId] = useState(localStorage.getItem('userId'));
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('userId', data.user_id);
      setToken(data.access_token);
      setUserId(data.user_id);
      return true;
    }
    return false;
  };

  const register = async (email, password, name) => {
    const response = await fetch('http://localhost:5000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name })
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('userId', data.user_id);
      setToken(data.access_token);
      setUserId(data.user_id);
      return true;
    }
    return false;
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setToken(null);
    setUserId(null);
    setUser(null);
  };

  return { token, userId, user, setUser, login, register, logout };
};

// ==================== COMPONENTS ====================

// Login Component
function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const { login, register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      let response;
      if (isRegister) {
        response = await fetch('http://localhost:5000/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name })
        });
      } else {
        response = await fetch('http://localhost:5000/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
      }
      
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userId', data.user_id);
        onLogin();
      } else {
        setError(data.error || (isRegister ? 'Registration failed' : 'Login failed'));
      }
    } catch (err) {
      setError(err.message || 'Network error');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>🏥 HealthPal Assistant</h1>
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

// Profile Setup Component
function ProfileSetup({ token, userId, onComplete }) {
  const [profile, setProfile] = useState({
    name: '',
    age: '',
    height_cm: '',
    weight_kg: '',
    blood_type: '',
    blood_sugar_fasting: '',
    blood_pressure_sys: '',
    blood_pressure_dia: '',
    job_title: '',
    job_stress_level: 'medium',
    sleep_goal_hours: '8',
    exercise_goal_minutes: '30',
    hobbies: '',
    likes: '',
    dislikes: '',
    has_menstrual_cycle: false,
    dietary_restrictions: '',
    allergies: '',
    meditation_preference: 'morning',
    video_reminder_interval: '3'
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:5000/api/user/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profile)
      });
      
      if (response.ok) {
        onComplete();
      }
    } catch (err) {
      console.error('Profile update failed:', err);
    }
  };

  return (
    <div className="profile-setup">
      <div className="profile-container">
        <h2>Set Your Health Profile</h2>
        <p className="subtitle">Help us understand your health needs</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-section">
            <h3>Basic Information</h3>
            
            <div className="form-row">
              <input
                type="text"
                name="name"
                placeholder="Full Name"
                value={profile.name}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-row">
              <input
                type="number"
                name="age"
                placeholder="Age"
                value={profile.age}
                onChange={handleChange}
              />
              <input
                type="text"
                name="blood_type"
                placeholder="Blood Type"
                value={profile.blood_type}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Physical Measurements</h3>
            
            <div className="form-row">
              <input
                type="number"
                name="height_cm"
                placeholder="Height (cm)"
                value={profile.height_cm}
                onChange={handleChange}
              />
              <input
                type="number"
                name="weight_kg"
                placeholder="Weight (kg)"
                value={profile.weight_kg}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-row">
              <input
                type="number"
                name="blood_sugar_fasting"
                placeholder="Fasting Blood Sugar (mg/dL)"
                value={profile.blood_sugar_fasting}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-row">
              <input
                type="number"
                name="blood_pressure_sys"
                placeholder="Blood Pressure Systolic"
                value={profile.blood_pressure_sys}
                onChange={handleChange}
              />
              <input
                type="number"
                name="blood_pressure_dia"
                placeholder="Blood Pressure Diastolic"
                value={profile.blood_pressure_dia}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Lifestyle</h3>
            
            <input
              type="text"
              name="job_title"
              placeholder="Job Title"
              value={profile.job_title}
              onChange={handleChange}
            />
            
            <select name="job_stress_level" value={profile.job_stress_level} onChange={handleChange}>
              <option value="low">Low Stress</option>
              <option value="medium">Medium Stress</option>
              <option value="high">High Stress</option>
            </select>
            
            <div className="form-row">
              <input
                type="number"
                name="sleep_goal_hours"
                placeholder="Sleep Goal (hours)"
                value={profile.sleep_goal_hours}
                onChange={handleChange}
              />
              <input
                type="number"
                name="exercise_goal_minutes"
                placeholder="Exercise Goal (minutes)"
                value={profile.exercise_goal_minutes}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Preferences & Health</h3>
            
            <textarea
              name="hobbies"
              placeholder="Hobbies"
              value={profile.hobbies}
              onChange={handleChange}
            />
            
            <textarea
              name="likes"
              placeholder="Foods/Activities You Like"
              value={profile.likes}
              onChange={handleChange}
            />
            
            <textarea
              name="dislikes"
              placeholder="Foods/Activities You Dislike"
              value={profile.dislikes}
              onChange={handleChange}
            />
            
            <div className="checkbox-group">
              <label>
                <input
                  type="checkbox"
                  name="has_menstrual_cycle"
                  checked={profile.has_menstrual_cycle}
                  onChange={handleChange}
                />
                Track Menstrual Cycle
              </label>
            </div>
            
            <textarea
              name="dietary_restrictions"
              placeholder="Dietary Restrictions"
              value={profile.dietary_restrictions}
              onChange={handleChange}
            />
            
            <textarea
              name="allergies"
              placeholder="Allergies"
              value={profile.allergies}
              onChange={handleChange}
            />
            
            <select name="meditation_preference" value={profile.meditation_preference} onChange={handleChange}>
              <option value="morning">Morning Meditation</option>
              <option value="evening">Evening Meditation</option>
              <option value="both">Both</option>
            </select>
            
            <input
              type="number"
              name="video_reminder_interval"
              placeholder="Video Reminder Interval (days)"
              value={profile.video_reminder_interval}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="btn-primary btn-large">
            Complete Profile Setup
          </button>
        </form>
      </div>
    </div>
  );
}

// Dashboard Component
function Dashboard({ token, userId, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [todayData, setTodayData] = useState(null);
  const [goals, setGoals] = useState(null);

  useEffect(() => {
    if (token) {
      fetchTodayData();
      fetchGoals();
    }
  }, [token]);

  const fetchTodayData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/health-checkin/today', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setTodayData(data);
      }
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const fetchGoals = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/daily-goals/today', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setGoals(data);
      }
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h1>🏥 HealthPal</h1>
        <div className="nav-tabs">
          <button
            className={activeTab === 'dashboard' ? 'active' : ''}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={activeTab === 'checkin' ? 'active' : ''}
            onClick={() => setActiveTab('checkin')}
          >
            Daily Check-in
          </button>
          <button
            className={activeTab === 'medications' ? 'active' : ''}
            onClick={() => setActiveTab('medications')}
          >
            Medications
          </button>
          <button
            className={activeTab === 'chat' ? 'active' : ''}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button
            className={activeTab === 'profile' ? 'active' : ''}
            onClick={() => setActiveTab('profile')}
          >
            Profile
          </button>
        </div>
      </nav>

      <div className="main-content">
        {activeTab === 'dashboard' && <DashboardView goals={goals} todayData={todayData} token={token} />}
        {activeTab === 'checkin' && <DailyCheckInView token={token} onComplete={fetchTodayData} />}
        {activeTab === 'medications' && <MedicationsView token={token} />}
        {activeTab === 'chat' && <ChatView token={token} />}
        {activeTab === 'profile' && <ProfileView token={token} />}
      </div>

      <button 
        onClick={onLogout}
        className="logout-btn"
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          padding: '10px 20px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          zIndex: 1000
        }}
      >
        Logout
      </button>
    </div>
  );
}

// Dashboard View Component
function DashboardView({ goals, todayData, token }) {
  return (
    <div className="dashboard-view">
      <h2>Today's Health Overview</h2>
      
      {goals && (
        <div className="goals-section">
          <h3>Daily Goals Progress</h3>
          <div className="goals-summary">
            <div className="summary-card">
              <p className="label">Completion</p>
              <p className="value">{Math.round(goals.summary?.completion_percentage || 0)}%</p>
              <p className="sublabel">{goals.summary?.completed_goals || 0} of {goals.summary?.total_goals || 0} completed</p>
            </div>
          </div>
          
          <div className="goals-list">
            {goals.goals && goals.goals.map(goal => (
              <div key={goal.id} className={`goal-item ${goal.completed ? 'completed' : ''}`}>
                <div className="goal-header">
                  <span className="goal-type">{goal.goal_type}</span>
                  <span className={`progress ${goal.completed ? 'done' : ''}`}>
                    {goal.current_value}/{goal.target_value} {goal.unit}
                  </span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${Math.min(goal.progress_percent || 0, 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {todayData && (
        <div className="today-summary">
          <h3>Today's Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span>Mood: </span>
              <strong>{todayData.mood || 'Not logged'}</strong>
            </div>
            <div className="summary-item">
              <span>Sleep: </span>
              <strong>{todayData.sleep_hours || '0'} hours</strong>
            </div>
            <div className="summary-item">
              <span>Water: </span>
              <strong>{todayData.water_intake_liters || '0'} liters</strong>
            </div>
            <div className="summary-item">
              <span>Exercise: </span>
              <strong>{todayData.exercise_minutes || '0'} minutes</strong>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Daily Check-In Component
function DailyCheckInView({ token, onComplete }) {
  const [formData, setFormData] = useState({
    mood: '',
    stress_level: 5,
    sleep_hours: '',
    water_intake_liters: '',
    exercise_minutes: '',
    meditation_minutes: '',
    notes: ''
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'stress_level' ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:5000/api/health-checkin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        setMessage('✅ Check-in saved successfully!');
        onComplete();
        setTimeout(() => setMessage(''), 3000);
      } else {
        const error = await response.json();
        setMessage(error.error);
      }
    } catch (err) {
      setMessage('Error saving check-in');
    }
  };

  return (
    <div className="checkin-view">
      <h2>Daily Health Check-In</h2>
      
      {message && <div className="message">{message}</div>}
      
      <form onSubmit={handleSubmit} className="checkin-form">
        <div className="form-group">
          <label>How are you feeling?</label>
          <select name="mood" value={formData.mood} onChange={handleChange} required>
            <option value="">Select mood</option>
            <option value="happy">😊 Happy</option>
            <option value="neutral">😐 Neutral</option>
            <option value="sad">😢 Sad</option>
            <option value="anxious">😰 Anxious</option>
            <option value="energetic">⚡ Energetic</option>
            <option value="tired">😴 Tired</option>
          </select>
        </div>

        <div className="form-group">
          <label>Stress Level (1-10)</label>
          <input
            type="range"
            name="stress_level"
            min="1"
            max="10"
            value={formData.stress_level}
            onChange={handleChange}
          />
          <span className="value">{formData.stress_level}</span>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Sleep Hours</label>
            <input
              type="number"
              name="sleep_hours"
              placeholder="Hours"
              value={formData.sleep_hours}
              onChange={handleChange}
              step="0.5"
            />
          </div>

          <div className="form-group">
            <label>Water Intake (Liters)</label>
            <input
              type="number"
              name="water_intake_liters"
              placeholder="Liters"
              value={formData.water_intake_liters}
              onChange={handleChange}
              step="0.5"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Exercise (Minutes)</label>
            <input
              type="number"
              name="exercise_minutes"
              placeholder="Minutes"
              value={formData.exercise_minutes}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Meditation (Minutes)</label>
            <input
              type="number"
              name="meditation_minutes"
              placeholder="Minutes"
              value={formData.meditation_minutes}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Notes</label>
          <textarea
            name="notes"
            placeholder="Any additional notes about your health today..."
            value={formData.notes}
            onChange={handleChange}
          />
        </div>

        <button type="submit" className="btn-primary btn-large">
          Save Check-in
        </button>
      </form>
    </div>
  );
}

// Medications Component
function MedicationsView({ token }) {
  const [medications, setMedications] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newMed, setNewMed] = useState({
    name: '',
    dosage: '',
    frequency: '',
    reason: '',
    stock_quantity: '',
    refill_threshold: '10'
  });

  useEffect(() => {
    fetchMedications();
  }, [token]);

  const fetchMedications = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/medications', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setMedications(data);
      }
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const handleAddMedication = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:5000/api/medications', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newMed)
      });
      
      if (response.ok) {
        setNewMed({
          name: '',
          dosage: '',
          frequency: '',
          reason: '',
          stock_quantity: '',
          refill_threshold: '10'
        });
        setShowForm(false);
        fetchMedications();
      }
    } catch (err) {
      console.error('Error adding medication:', err);
    }
  };

  const handleLogIntake = async (medId) => {
    try {
      await fetch(`http://localhost:5000/api/medications/${medId}/intake`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ skipped: false })
      });
      fetchMedications();
    } catch (err) {
      console.error('Error logging intake:', err);
    }
  };

  return (
    <div className="medications-view">
      <h2>Medications</h2>
      
      <button 
        className="btn-primary"
        onClick={() => setShowForm(!showForm)}
      >
        {showForm ? 'Cancel' : '+ Add Medication'}
      </button>

      {showForm && (
        <form onSubmit={handleAddMedication} className="medication-form">
          <input
            type="text"
            placeholder="Medication Name"
            value={newMed.name}
            onChange={(e) => setNewMed({...newMed, name: e.target.value})}
            required
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
            required
          />
          
          <input
            type="text"
            placeholder="Reason"
            value={newMed.reason}
            onChange={(e) => setNewMed({...newMed, reason: e.target.value})}
          />
          
          <input
            type="number"
            placeholder="Stock Quantity"
            value={newMed.stock_quantity}
            onChange={(e) => setNewMed({...newMed, stock_quantity: e.target.value})}
            required
          />
          
          <button type="submit" className="btn-primary">Add Medication</button>
        </form>
      )}

      <div className="medications-list">
        {medications.map(med => (
          <div key={med.id} className="medication-card">
            <div className="med-header">
              <h4>{med.name}</h4>
              <span className={`stock ${med.stock_quantity < med.refill_threshold ? 'low' : ''}`}>
                Stock: {med.stock_quantity}
              </span>
            </div>
            <p><strong>Dosage:</strong> {med.dosage}</p>
            <p><strong>Frequency:</strong> {med.frequency}</p>
            <p><strong>Reason:</strong> {med.reason}</p>
            <button 
              className="btn-secondary"
              onClick={() => handleLogIntake(med.id)}
            >
              ✓ Log Intake
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

// Chat Component
function ChatView({ token }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchChatHistory();
  }, [token]);

  const fetchChatHistory = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/chat/history', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      }
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/api/chat', {
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
          { role: 'user', message: data.user_message, id: Date.now() },
          { role: 'assistant', message: data.assistant_response, id: Date.now() + 1 }
        ]);
        setInput('');
      }
    } catch (err) {
      console.error('Error sending message:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-view">
      <h2>Chat with HealthPal Assistant</h2>
      
      <div className="chat-messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.message}
            </div>
          </div>
        ))}
        {loading && <div className="message assistant"><span className="typing">Thinking...</span></div>}
      </div>

      <form onSubmit={handleSendMessage} className="chat-input-form">
        <input
          type="text"
          placeholder="Ask me about your health..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="btn-primary">
          Send
        </button>
      </form>
    </div>
  );
}

// Profile View Component
function ProfileView({ token }) {
  const [profile, setProfile] = useState(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const fetchProfile = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:5000/api/user/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
        setFormData(data);
        setError('');
      } else {
        // handle non-ok responses
        let errMsg = `Error ${response.status}`;
        try {
          const body = await response.json();
          errMsg = body.error || body.message || errMsg;
        } catch (_) {}

        // If unauthorized, suggest re-login
        if (response.status === 401 || response.status === 403) {
          errMsg = 'Unauthorized. Please logout and login again.';
        }

        setError(errMsg);
        setProfile(null);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError('Network error while loading profile');
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch('http://localhost:5000/api/user/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setEditing(false);
        fetchProfile();
      } else {
        const body = await response.json();
        setError(body.error || 'Failed to save profile');
      }
    } catch (err) {
      console.error('Error saving profile:', err);
      setError('Network error while saving profile');
    }
  };

  if (loading) return <div className="loading">Loading profile...</div>;

  return (
    <div className="profile-view">
      <h2>Your Health Profile</h2>

      {error && (
        <div className="error-message" style={{ marginBottom: 12 }}>
          {error} <button className="link-btn" onClick={fetchProfile}>Retry</button>
        </div>
      )}

      <button 
        className="btn-primary"
        onClick={() => setEditing(!editing)}
      >
        {editing ? 'Cancel' : '✏️ Edit Profile'}
      </button>

      {editing ? (
        <form onSubmit={handleSaveProfile} className="profile-form">
          <h3>Personal Information</h3>
          <input
            type="text"
            placeholder="Name"
            value={formData.name || ''}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
          />
          <input
            type="number"
            placeholder="Age"
            value={formData.age || ''}
            onChange={(e) => setFormData({...formData, age: e.target.value})}
          />
          
          <h3>Health Measurements</h3>
          <input
            type="number"
            placeholder="Height (cm)"
            value={formData.height_cm || ''}
            onChange={(e) => setFormData({...formData, height_cm: e.target.value})}
          />
          <input
            type="number"
            placeholder="Weight (kg)"
            value={formData.weight_kg || ''}
            onChange={(e) => setFormData({...formData, weight_kg: e.target.value})}
          />
          
          <button type="submit" className="btn-primary">Save Changes</button>
        </form>
      ) : (
        <div className="profile-display">
          <div className="profile-section">
            <h3>Personal Information</h3>
            <p><strong>Name:</strong> {profile.name}</p>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Age:</strong> {profile.age || 'Not set'}</p>
            <p><strong>Job:</strong> {profile.job_title || 'Not set'}</p>
          </div>

          <div className="profile-section">
            <h3>Health Measurements</h3>
            <p><strong>Height:</strong> {profile.height_cm} cm</p>
            <p><strong>Weight:</strong> {profile.weight_kg} kg</p>
            <p><strong>Blood Type:</strong> {profile.blood_type || 'Not set'}</p>
            <p><strong>Blood Pressure:</strong> {profile.blood_pressure}</p>
          </div>

          <div className="profile-section">
            <h3>Health Goals</h3>
            <p><strong>Sleep Goal:</strong> {profile.sleep_goal_hours} hours</p>
            <p><strong>Exercise Goal:</strong> {profile.exercise_goal_minutes} minutes</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userId, setUserId] = useState(localStorage.getItem('userId'));
  const [showProfile, setShowProfile] = useState(false);

  const handleLogin = () => {
    setToken(localStorage.getItem('token'));
    setUserId(localStorage.getItem('userId'));
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setToken(null);
    setUserId(null);
    setIsLoggedIn(false);
    setShowProfile(false);
  };

  if (!isLoggedIn && !token) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div>
      {showProfile ? (
        <ProfileSetup token={token} userId={userId} onComplete={() => setShowProfile(false)} />
      ) : (
        <Dashboard token={token} userId={userId} onLogout={handleLogout} />
      )}
    </div>
  );
}

