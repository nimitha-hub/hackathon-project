# HealMate Deployment Guide

## Prerequisites
- GitHub account with your code pushed
- API keys ready (OpenAI, Google AI, Gmail app password)

---

## Option 1: Deploy on Render (Free & Recommended)

### Step 1: Deploy Backend

1. **Sign up at [Render](https://render.com)**
   - Use your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `nimitha-hub/hackathon-project`
   - Configure:
     - **Name**: `healmate-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
     - **Instance Type**: Free

3. **Add Environment Variables**
   Go to "Environment" tab and add:
   ```
   FLASK_ENV=production
   JWT_SECRET_KEY=your-jwt-secret-key
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   GOOGLE_API_KEY=your-google-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Copy your backend URL (e.g., `https://healmate-backend.onrender.com`)

### Step 2: Deploy Frontend

1. **Create Another Web Service**
   - Click "New +" → "Static Site"
   - Select same repository
   - Configure:
     - **Name**: `healmate-frontend`
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `build`

2. **Add Environment Variable**
   ```
   REACT_APP_API_URL=https://healmate-backend.onrender.com
   ```
   (Use the URL from Step 1)

3. **Deploy**
   - Click "Create Static Site"
   - Wait 2-3 minutes
   - Your app will be live at `https://healmate-frontend.onrender.com`

---

## Option 2: Deploy on Vercel + Railway

### Backend on Railway

1. **Sign up at [Railway](https://railway.app)**
2. **New Project** → "Deploy from GitHub repo"
3. Select `hackathon-project/backend`
4. Add environment variables (same as above)
5. Railway will auto-detect Flask and deploy
6. Copy your backend URL

### Frontend on Vercel

1. **Sign up at [Vercel](https://vercel.com)**
2. **New Project** → Import from GitHub
3. Select `hackathon-project`
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Create React App
   - **Environment Variable**: `REACT_APP_API_URL=<your-railway-backend-url>`
5. Deploy

---

## Option 3: Deploy on Heroku

### Backend

```bash
# Install Heroku CLI first
cd backend
heroku login
heroku create healmate-backend
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=your-secret-key
# ... add all other env vars
git push heroku main
```

### Frontend

```bash
cd frontend
heroku create healmate-frontend
heroku buildpacks:set heroku/nodejs
heroku config:set REACT_APP_API_URL=https://healmate-backend.herokuapp.com
git push heroku main
```

---

## Post-Deployment Checklist

### 1. Update CORS Settings

Edit `backend/app.py` to allow your frontend domain:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://healmate-frontend.onrender.com",  # Add your domain
            "http://localhost:3000"
        ]
    }
})
```

### 2. Test Your Deployment

- Visit your frontend URL
- Register a new account
- Test login
- Try the AI chat
- Check profile updates

### 3. Commit & Push Changes

```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError"**
- Check `requirements.txt` includes all packages
- Verify build logs on hosting platform

**Error: "500 Internal Server Error"**
- Check environment variables are set correctly
- View logs: `heroku logs --tail` or Render dashboard logs

**Database issues**
- SQLite works for small deployments
- For production, consider PostgreSQL (Railway/Render offer free tier)

### Frontend Issues

**API calls failing**
- Verify `REACT_APP_API_URL` is set correctly
- Check browser console for CORS errors
- Ensure backend allows your frontend domain

**Build fails**
- Run `npm install` locally to check for errors
- Check Node version compatibility

---

## Upgrade to PostgreSQL (Optional)

For production use, replace SQLite:

1. **Add to requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```

2. **Update app.py**:
   ```python
   DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///healmate.db')
   if DATABASE_URL.startswith("postgres://"):
       DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
   
   app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
   ```

3. **Add PostgreSQL on Render/Railway**:
   - Both platforms offer free PostgreSQL databases
   - Copy the database URL to environment variables

---

## Cost Estimate

| Service | Free Tier | Paid Plans |
|---------|-----------|------------|
| **Render** | 750 hrs/month | $7+/month |
| **Railway** | $5 free credit/month | Pay as you go |
| **Vercel** | Unlimited | $20+/month for team |
| **Heroku** | No free tier | $7+/month |

**Recommendation**: Start with Render free tier for both frontend and backend.

---

## Quick Start Commands

```bash
# Commit deployment files
cd "C:\Users\NIMITHA\Desktop\Hackathon"
git add backend/requirements.txt backend/Procfile backend/runtime.txt backend/render.yaml
git add frontend/.env.production frontend/src/App.jsx
git commit -m "Add deployment configuration"
git push origin main

# Then follow Render steps above
```

---

## Security Notes

✅ Never commit `.env` files with real secrets  
✅ Use environment variables on hosting platforms  
✅ Rotate API keys if accidentally exposed  
✅ Enable HTTPS (automatic on most platforms)  
✅ Use strong JWT secret keys  
✅ Gmail app passwords (not main password)  

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/3.0.x/deploying/

Your app is now ready to deploy! 🚀
