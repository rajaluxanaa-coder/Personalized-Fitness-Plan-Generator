"""
Authentication utilities for FitPlan-AI
"""

import hashlib
import os

def hash_password(password):
    """Hash a password using SHA-256 with salt"""
    salt = os.urandom(32).hex()
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    try:
        salt, hash_value = hashed_password.split('$')
        check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return check_hash == hash_value
    except:
        return False
