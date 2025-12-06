import React from 'react';

export default function LandingPage({ onGetStarted }) {
  return (
    <div className="landing-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              <span className="gradient-text">HealMate</span>
            </h1>
            <p className="hero-subtitle">Your AI-Powered Personal Health Companion</p>
            <p className="hero-description">
              Take control of your health journey with intelligent scheduling, personalized recommendations, 
              and 24/7 AI health assistance. Never miss a medication, stay hydrated, and achieve your wellness goals.
            </p>
            <button className="cta-button" onClick={onGetStarted}>
              Get Started - It's Free
            </button>
          </div>
          
          <div className="hero-image">
            <div className="floating-card card-1">
              <div className="card-icon">💊</div>
              <div className="card-text">
                <h4>Medication Reminders</h4>
                <p>Never miss a dose</p>
              </div>
            </div>
            <div className="floating-card card-2">
              <div className="card-icon">🤖</div>
              <div className="card-text">
                <h4>AI Health Coach</h4>
                <p>24/7 personalized guidance</p>
              </div>
            </div>
            <div className="floating-card card-3">
              <div className="card-icon">📊</div>
              <div className="card-text">
                <h4>Progress Tracking</h4>
                <p>Visualize your journey</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">Everything You Need for Better Health</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI Health Assistant</h3>
            <p>Chat with your personal AI health coach for diet plans, workout routines, and health advice tailored to you.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📅</div>
            <h3>Smart Daily Schedule</h3>
            <p>Automatically generated daily routines based on your goals, including meals, water breaks, and exercise times.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Daily Goals Tracker</h3>
            <p>Track medications, water intake, and meals with visual progress indicators. Stay motivated with real-time completion stats.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔔</div>
            <h3>Smart Notifications</h3>
            <p>Timely reminders for medications, water intake, meals, and breaks. Never forget your health routine again.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💪</div>
            <h3>Personalized Workout Plans</h3>
            <p>Get custom exercise routines based on your fitness level, health conditions, and goals.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📈</div>
            <h3>Health Analytics</h3>
            <p>Visualize your progress with weekly reports showing medication adherence, hydration, and goal completion.</p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <h2 className="section-title">How It Works</h2>
        <div className="steps-container">
          <div className="step-item">
            <div className="step-number">1</div>
            <h3>Set Up Your Profile</h3>
            <p>Enter your health details, medications, sleep goals, and dietary preferences. Takes just 2 minutes.</p>
          </div>
          <div className="step-item">
            <div className="step-number">2</div>
            <h3>Get Your Personalized Plan</h3>
            <p>HealMate's AI creates a custom daily schedule and health plan tailored to your unique needs.</p>
          </div>
          <div className="step-item">
            <div className="step-number">3</div>
            <h3>Stay on Track</h3>
            <p>Follow your schedule, chat with AI for guidance, and watch your health goals become reality.</p>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="benefits-section">
        <h2 className="section-title">Why Choose HealMate?</h2>
        <div className="benefits-list">
          <div className="benefit-item">
            <div className="benefit-icon">✓</div>
            <div className="benefit-content">
              <h3>Completely Free</h3>
              <p>No hidden fees, no subscriptions. All features available to everyone, forever.</p>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon">✓</div>
            <div className="benefit-content">
              <h3>Privacy First</h3>
              <p>Your health data is secure and never shared. You're in complete control.</p>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon">✓</div>
            <div className="benefit-content">
              <h3>Always Available</h3>
              <p>24/7 access to your AI health coach and personalized health dashboard from any device.</p>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon">✓</div>
            <div className="benefit-content">
              <h3>Science-Backed</h3>
              <p>Recommendations based on medical guidelines and health best practices.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2>Ready to Transform Your Health?</h2>
        <p>Join thousands taking control of their wellness journey</p>
        <button className="cta-button-large" onClick={onGetStarted}>
          Start Your Health Journey Today
        </button>
        <p className="cta-note">No credit card required • Set up in 2 minutes</p>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>&copy; 2024 HealMate. Your partner in health and wellness.</p>
      </footer>
    </div>
  );
}
