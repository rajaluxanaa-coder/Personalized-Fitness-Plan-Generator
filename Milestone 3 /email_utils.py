"""
Email utilities for sending OTP
FitPlan-AI Milestone 3
"""

import os
import sendgrid
from sendgrid.helpers.mail import Mail

def send_otp_email(recipient_email, otp):
    """
    Send OTP via email using SendGrid
    """
    try:
        # Get SendGrid API key from environment
        sg_api_key = os.getenv('SENDGRID_API_KEY')
        
        if not sg_api_key:
            print("❌ SendGrid API key not found")
            # For development, just print OTP
            print(f"📧 OTP for {recipient_email}: {otp}")
            return True
        
        # Create email message
        message = Mail(
            from_email=os.getenv('EMAIL_USER', 'noreply@fitplan-ai.com'),
            to_emails=recipient_email,
            subject='FitPlan-AI - Your Verification Code',
            plain_text_content=f'''Welcome to FitPlan-AI!

Your verification code is: {otp}

This code will expire in 10 minutes.

Thanks,
FitPlan-AI Team'''
        )
        
        # Send via SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
        response = sg.send(message)
        
        if response.status_code in [200, 202]:
            print(f"✅ OTP sent to {recipient_email}")
            return True
        else:
            print(f"❌ Failed to send OTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
