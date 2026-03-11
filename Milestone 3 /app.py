"""
Milestone 3: Login System with OTP Verification
FitPlan-AI
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import db, User, init_db
from auth import verify_password, hash_password
from email_utils import send_otp_email
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///fitness.db')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Store OTP temporarily (in production, use Redis)
otp_storage = {}

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Home page with login/signup options"""
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'Email already registered'})
        
        # Hash password and create user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            password=hashed_password
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'User created successfully'})
        
    except Exception as e:
        print(f"Error in signup: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/login', methods=['POST'])
def login():
    """User login endpoint - verifies credentials"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user or not verify_password(password, user.password):
            return jsonify({'success': False, 'error': 'Invalid email or password'})
        
        # Store user ID in session
        session['user_id'] = user.id
        session['email'] = user.email
        
        # Generate and send OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp
        
        # Send OTP via email
        send_otp_email(email, otp)
        
        return jsonify({'success': True, 'message': 'OTP sent to your email'})
        
    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    """OTP verification endpoint"""
    try:
        data = request.json
        email = data.get('email')
        otp = data.get('otp')
        
        # Verify OTP
        if email in otp_storage and otp_storage[email] == otp:
            # Clear OTP after successful verification
            del otp_storage[email]
            return jsonify({'success': True, 'message': 'OTP verified successfully'})
        
        return jsonify({'success': False, 'error': 'Invalid OTP'})
        
    except Exception as e:
        print(f"Error in OTP verification: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dashboard')
def dashboard():
    """Protected dashboard - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    """Logout endpoint"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/init-db')
def init_db_route():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
    return "Database initialized successfully!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
