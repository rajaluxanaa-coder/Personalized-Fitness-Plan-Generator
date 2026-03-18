"""
FitPlan-AI - Milestone 4: Application Finalization & Deployment
File: app.py (Relevant Sections Only)
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
import requests
import json
from datetime import datetime, timedelta
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Rate limiting for OTP endpoints
limiter = Limiter(app=app, key_func=get_remote_address)

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///fitness.db')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
mail = Mail(app)

# ======================================================
# TASK 1: INPUT VALIDATION FUNCTIONS
# ======================================================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None

def validate_age(age):
    """Validate age is between 15 and 100"""
    try:
        age = int(age)
        if age < 15 or age > 100:
            return False, "Age must be between 15 and 100 years"
        return True, None
    except:
        return False, "Age must be a valid number"

def validate_weight(weight):
    """Validate weight is between 20 and 300 kg"""
    try:
        weight = float(weight)
        if weight < 20 or weight > 300:
            return False, "Weight must be between 20 and 300 kg"
        return True, None
    except:
        return False, "Weight must be a valid number"

def validate_height(height):
    """Validate height is between 100 and 250 cm"""
    try:
        height = float(height)
        if height < 100 or height > 250:
            return False, "Height must be between 100 and 250 cm"
        return True, None
    except:
        return False, "Height must be a valid number"

def validate_fitness_level(level):
    """Validate fitness level is valid"""
    valid_levels = ['beginner', 'intermediate', 'advanced']
    if level not in valid_levels:
        return False, "Fitness level must be beginner, intermediate, or advanced"
    return True, None

def validate_goal(goal):
    """Validate fitness goal is valid"""
    valid_goals = ['weight_loss', 'muscle_gain', 'strength', 'endurance', 'toning', 'general']
    if goal not in valid_goals:
        return False, "Invalid fitness goal selected"
    return True, None

# ======================================================
# TASK 2: OTP STORAGE WITH EXPIRY
# ======================================================

otp_storage = {}  # Temporary storage for OTPs

def is_otp_expired(timestamp, expiry_minutes=10):
    """Check if OTP is expired (10 minute expiry)"""
    return datetime.now() - timestamp > timedelta(minutes=expiry_minutes)

# ======================================================
# TASK 3: AUTHENTICATION FLOW WITH VALIDATION
# ======================================================

@app.route('/check-email', methods=['POST'])
def check_email():
    """Check if email already exists with validation"""
    data = request.json
    email = data.get('email')
    
    valid, error = validate_email(email)
    if not valid:
        return jsonify({'exists': False, 'valid': False, 'message': error})
    
    from models import User
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None, 'valid': True})

@app.route('/send-otp', methods=['POST'])
@limiter.limit("5 per minute")
def send_otp():
    """Send OTP with rate limiting and expiry"""
    try:
        email = request.json.get('email')
        
        valid, error = validate_email(email)
        if not valid:
            return jsonify({'success': False, 'message': error})
        
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = {
            'otp': otp,
            'timestamp': datetime.now()
        }
        
        # Send via email (implementation in email_utils.py)
        from email_utils import send_otp_email
        success = send_otp_email(email, otp)
        
        if success:
            return jsonify({'success': True, 'message': 'OTP sent'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send OTP'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP with expiry check"""
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    
    if email not in otp_storage:
        return jsonify({'success': False, 'message': 'No OTP found'})
    
    stored = otp_storage[email]
    
    if is_otp_expired(stored['timestamp']):
        del otp_storage[email]
        return jsonify({'success': False, 'message': 'OTP expired'})
    
    if stored['otp'] == otp:
        session['email'] = email
        from models import User
        user = User.query.filter_by(email=email).first()
        if user:
            session['user_id'] = user.id
            return jsonify({'success': True, 'new_user': False})
        else:
            return jsonify({'success': True, 'new_user': True})
    
    return jsonify({'success': False, 'message': 'Invalid OTP'})

@app.route('/resend-otp', methods=['POST'])
@limiter.limit("3 per minute")
def resend_otp():
    """Resend OTP with rate limiting"""
    email = request.json.get('email')
    
    if email not in otp_storage:
        return jsonify({'success': False, 'message': 'No OTP found'})
    
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {
        'otp': otp,
        'timestamp': datetime.now()
    }
    
    from email_utils import send_otp_email
    success = send_otp_email(email, otp)
    
    if success:
        return jsonify({'success': True, 'message': 'OTP resent'})
    else:
        return jsonify({'success': False, 'message': 'Failed to resend OTP'})

@app.route('/direct-signup', methods=['POST'])
def direct_signup():
    """Create new user with input validation"""
    try:
        data = request.json
        
        # Validate all inputs
        valid, error = validate_email(data['email'])
        if not valid:
            return jsonify({'success': False, 'error': error})
        
        valid, error = validate_age(data['age'])
        if not valid:
            return jsonify({'success': False, 'error': error})
        
        valid, error = validate_weight(data['weight'])
        if not valid:
            return jsonify({'success': False, 'error': error})
        
        valid, error = validate_height(data['height'])
        if not valid:
            return jsonify({'success': False, 'error': error})
        
        valid, error = validate_fitness_level(data['fitness_level'])
        if not valid:
            return jsonify({'success': False, 'error': error})
        
        from models import User
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'Email already registered'})
        
        user = User(
            email=data['email'],
            name=data['name'],
            age=int(data['age']),
            weight=float(data['weight']),
            height=float(data['height']),
            fitness_level=data['fitness_level']
        )
        
        db.session.add(user)
        db.session.commit()
        
        session['email'] = data['email']
        session['user_id'] = user.id
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ======================================================
# TASK 4: AI WORKOUT GENERATION WITH ERROR HANDLING
# ======================================================

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    """Generate AI workout with fallback error handling"""
    try:
        data = request.json
        from models import User
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        goal = data.get('goal', 'strength')
        level = data.get('level', 'beginner')
        equipment = data.get('equipment', 'bodyweight')
        
        # Build prompt (from prompt_builder.py)
        from prompt_builder import build_workout_prompt
        prompt = build_workout_prompt(user, goal, level, equipment)
        
        # Generate with fallback (from model_api.py)
        from model_api import generate_workout_with_ai
        schedule = generate_workout_with_ai(prompt, user, goal, level, equipment)
        
        # Save schedule
        from models import WorkoutSchedule
        workout_schedule = WorkoutSchedule(
            user_id=user.id,
            schedule_data=schedule
        )
        db.session.add(workout_schedule)
        db.session.commit()
        
        return jsonify({'success': True, 'schedule': schedule})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ======================================================
# TASK 5: DASHBOARD AND NAVIGATION
# ======================================================

@app.route('/dashboard')
def dashboard():
    """Dashboard page with smooth navigation"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    from models import User
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/schedule')
def schedule():
    """Schedule page with improved UI"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    from models import User
    user = User.query.get(session['user_id'])
    return render_template('schedule.html', user=user)

# ======================================================
# TASK 6: DATABASE INITIALIZATION
# ======================================================

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
