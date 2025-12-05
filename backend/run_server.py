"""Run Flask app with Waitress WSGI server (Windows compatible)"""

from app import app

if __name__ == '__main__':
    from waitress import serve
    
    with app.app_context():
        from app import db
        db.create_all()
    
    print("Starting HealMate Backend with Waitress...")
    print("Backend running on http://127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000, threads=10)

