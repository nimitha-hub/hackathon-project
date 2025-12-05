#!/bin/bash
# HealMate Quick Test Script
# Run these commands to test all integrations

echo "=========================================="
echo "HealMate Integration Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Checking Environment Setup${NC}"
echo "=================================="

# Check if Python is installed
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 found$(python3 --version)${NC}"
else
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi

# Check if Node is installed
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓ Node.js found ($(node --version))${NC}"
else
    echo -e "${RED}✗ Node.js not found${NC}"
    exit 1
fi

# Check if backend .env exists
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓ Backend .env file found${NC}"
    # Check required variables
    if grep -q "GOOGLE_API_KEY=" backend/.env && grep -q "SENDER_EMAIL=" backend/.env; then
        echo -e "${GREEN}✓ Required environment variables configured${NC}"
    else
        echo -e "${RED}✗ Missing required environment variables (GOOGLE_API_KEY, SENDER_EMAIL)${NC}"
        echo "  Please edit backend/.env with your API keys"
    fi
else
    echo -e "${RED}✗ Backend .env file not found${NC}"
    echo "  Run: cp backend/.env.example backend/.env"
    echo "  Then edit with your API keys"
fi

echo ""
echo -e "${BLUE}2. Checking Python Dependencies${NC}"
echo "=================================="

cd backend

# Check Flask
python3 -c "import flask; print(f'✓ Flask {flask.__version__}')" 2>/dev/null || echo -e "${RED}✗ Flask not installed${NC}"

# Check Flask-SQLAlchemy
python3 -c "import flask_sqlalchemy; print('✓ Flask-SQLAlchemy installed')" 2>/dev/null || echo -e "${RED}✗ Flask-SQLAlchemy not installed${NC}"

# Check google-generativeai
python3 -c "import google.generativeai; print('✓ Google Generative AI installed')" 2>/dev/null || echo -e "${RED}✗ Google Generative AI not installed (required for chat)${NC}"

# Check APScheduler
python3 -c "import apscheduler; print('✓ APScheduler installed')" 2>/dev/null || echo -e "${RED}✗ APScheduler not installed (required for reminders)${NC}"

# Check Flask-JWT-Extended
python3 -c "import flask_jwt_extended; print('✓ Flask-JWT-Extended installed')" 2>/dev/null || echo -e "${RED}✗ Flask-JWT-Extended not installed${NC}"

cd ..

echo ""
echo -e "${BLUE}3. Checking Frontend Dependencies${NC}"
echo "=================================="

cd frontend

if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓ node_modules directory found${NC}"
else
    echo -e "${RED}✗ node_modules not found, run: npm install${NC}"
fi

# Check package.json
if [ -f "package.json" ]; then
    echo -e "${GREEN}✓ package.json found${NC}"
else
    echo -e "${RED}✗ package.json not found${NC}"
fi

cd ..

echo ""
echo -e "${BLUE}4. API Endpoint Status Check${NC}"
echo "=================================="

echo "Checking if backend is running on port 5000..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}✗ Backend is not running${NC}"
    echo "  Start it with: cd backend && python app.py"
fi

echo ""
echo -e "${BLUE}5. Database Check${NC}"
echo "=================================="

cd backend
if [ -f "instance/health_assistant.db" ]; then
    echo -e "${GREEN}✓ SQLite database found${NC}"
    # Get table count
    tables=$(python3 -c "import sqlite3; conn = sqlite3.connect('instance/health_assistant.db'); cursor = conn.cursor(); cursor.execute(\"SELECT COUNT(*) FROM sqlite_master WHERE type='table'\"); print(cursor.fetchone()[0])" 2>/dev/null)
    echo -e "${GREEN}✓ Database has $tables tables${NC}"
else
    echo -e "${RED}✗ Database not found (will be created on first backend run)${NC}"
fi
cd ..

echo ""
echo -e "${BLUE}6. Quick Start Commands${NC}"
echo "=================================="

cat << 'EOF'

# Terminal 1: Start Backend
cd backend
python app.py

# Terminal 2: Start Frontend
cd frontend
npm start

# Test Cases:
# 1. Register: Create new account
# 2. Profile: Fill all fields + add medication
# 3. Chat: Ask "What should I eat?"
# 4. Email: Send weekly report
# 5. Check logs for scheduler messages

# Environment Variables to Set:
# GOOGLE_API_KEY=<from google-ai-studio>
# SENDER_EMAIL=<your-gmail>
# SENDER_PASSWORD=<app-password-not-regular-password>

EOF

echo ""
echo -e "${BLUE}7. Testing Checklist${NC}"
echo "=================================="

cat << 'EOF'

[ ] Backend starts without errors
[ ] Frontend loads on localhost:3000
[ ] Can register new account
[ ] Profile setup page collects all fields
[ ] Dashboard shows schedule table
[ ] Chat responds with AI reply (3-5 sec wait)
[ ] Email button sends report to inbox
[ ] Console logs show scheduler activity
[ ] No CORS errors in browser console
[ ] No 401 Unauthorized errors
[ ] Responsive design works on mobile

EOF

echo ""
echo -e "${GREEN}=========================================="
echo "Test suite complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Ensure all dependencies are installed"
echo "2. Set environment variables in backend/.env"
echo "3. Run: cd backend && python app.py"
echo "4. Run: cd frontend && npm start"
echo "5. Follow testing checklist above"
echo ""
