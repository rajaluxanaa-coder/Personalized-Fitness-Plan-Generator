"""
FitPlan-AI - Milestone 4: Application Finalization & Deployment
File: database.py - Database Models with Input Validation Support
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ======================================================
# USER MODEL WITH CONSTRAINTS FOR VALIDATION
# ======================================================

class User(db.Model):
    """User accounts with validation constraints"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Fields with validation (to be checked at application level)
    age = db.Column(db.Integer)  # Validated: 15-100
    weight = db.Column(db.Float)  # Validated: 20-300
    height = db.Column(db.Float)  # Validated: 100-250
    fitness_level = db.Column(db.String(50))  # Validated: beginner/intermediate/advanced
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'


# ======================================================
# OTP STORAGE MODEL (FOR TRACKING OTP ATTEMPTS)
# ======================================================

class OTPRecord(db.Model):
    """Track OTP generation for rate limiting and expiry"""
    __tablename__ = 'otp_records'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, index=True)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)
    
    def is_expired(self, expiry_minutes=10):
        """Check if OTP is expired"""
        from datetime import timedelta
        return datetime.utcnow() - self.created_at > timedelta(minutes=expiry_minutes)


# ======================================================
# WORKOUT SCHEDULE MODEL (FOR AI GENERATION)
# ======================================================

class WorkoutSchedule(db.Model):
    """Store AI-generated workout plans"""
    __tablename__ = 'workout_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_data = db.Column(db.Text)  # The generated workout plan
    goal = db.Column(db.String(50))  # Store the goal used for generation
    level = db.Column(db.String(20))  # Store the level used
    equipment = db.Column(db.String(100))  # Store equipment used
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='schedules')


# ======================================================
# ERROR LOG MODEL (FOR GRACEFUL ERROR HANDLING)
# ======================================================

class ErrorLog(db.Model):
    """Log errors for debugging and monitoring"""
    __tablename__ = 'error_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ======================================================
# HELPER FUNCTIONS FOR MILESTONE 4
# ======================================================

def validate_user_data(age, weight, height, fitness_level):
    """
    Validation helper - matches the validation in app.py
    Showcases input validation requirement
    """
    errors = []
    
    # Age validation (15-100)
    try:
        age_val = int(age)
        if age_val < 15 or age_val > 100:
            errors.append("Age must be between 15 and 100")
    except:
        errors.append("Age must be a valid number")
    
    # Weight validation (20-300 kg)
    try:
        weight_val = float(weight)
        if weight_val < 20 or weight_val > 300:
            errors.append("Weight must be between 20 and 300 kg")
    except:
        errors.append("Weight must be a valid number")
    
    # Height validation (100-250 cm)
    try:
        height_val = float(height)
        if height_val < 100 or height_val > 250:
            errors.append("Height must be between 100 and 250 cm")
    except:
        errors.append("Height must be a valid number")
    
    # Fitness level validation
    valid_levels = ['beginner', 'intermediate', 'advanced']
    if fitness_level not in valid_levels:
        errors.append("Fitness level must be beginner, intermediate, or advanced")
    
    return errors


def get_user_stats_for_analytics(user_id):
    """
    Get user statistics for analytics dashboard
    Showcases data retrieval for UI
    """
    from sqlalchemy import func
    
    workouts = WorkoutLog.query.filter_by(user_id=user_id).count()
    meals = MealLog.query.filter_by(user_id=user_id).count()
    
    total_calories = db.session.query(
        func.sum(WorkoutLog.calories_burned)
    ).filter_by(user_id=user_id).scalar() or 0
    
    total_minutes = db.session.query(
        func.sum(WorkoutLog.duration)
    ).filter_by(user_id=user_id).scalar() or 0
    
    return {
        'workouts': workouts,
        'meals': meals,
        'calories_burned': total_calories,
        'minutes': total_minutes
    }


def get_recent_activity(user_id, limit=5):
    """
    Get recent user activity for dashboard
    Showcases data retrieval for UI improvements
    """
    workouts = WorkoutLog.query.filter_by(user_id=user_id)\
        .order_by(WorkoutLog.date.desc())\
        .limit(limit).all()
    
    meals = MealLog.query.filter_by(user_id=user_id)\
        .order_by(MealLog.date.desc())\
        .limit(limit).all()
    
    activity = []
    
    for w in workouts:
        activity.append({
            'type': 'workout',
            'title': w.workout_name,
            'date': w.date.strftime('%Y-%m-%d'),
            'details': f"{w.duration} min • {w.calories_burned} cal"
        })
    
    for m in meals:
        activity.append({
            'type': 'meal',
            'title': m.food_name,
            'date': m.date.strftime('%Y-%m-%d'),
            'details': f"{m.calories} cal"
        })
    
    # Sort by date (newest first)
    activity.sort(key=lambda x: x['date'], reverse=True)
    
    return activity[:limit]


# ======================================================
# MODELS NEEDED FOR OTHER FEATURES (REFERENCED BUT NOT CORE TO MILESTONE 4)
# ======================================================

class WorkoutLog(db.Model):
    """Record completed workouts"""
    __tablename__ = 'workout_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    workout_name = db.Column(db.String(200))
    duration = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    exercises = db.Column(db.Text)
    mood = db.Column(db.String(50))


class MealLog(db.Model):
    """Record daily meals"""
    __tablename__ = 'meal_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    meal_type = db.Column(db.String(50))
    food_name = db.Column(db.String(200))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fats = db.Column(db.Float)


# ======================================================
# DATABASE INITIALIZATION
# ======================================================

def init_db():
    """Initialize database tables"""
    db.create_all()
    print("✅ Database initialized for Milestone 4")
    print("   Features: Input validation, OTP tracking, Error logging")
