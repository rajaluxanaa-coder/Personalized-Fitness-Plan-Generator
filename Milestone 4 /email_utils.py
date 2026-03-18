"""
Email utilities for sending OTP via SendGrid
"""

import os
import sendgrid
from sendgrid.helpers.mail import Mail

def send_otp_email(recipient_email, otp):
    """Send OTP via SendGrid"""
    try:
        sg_api_key = os.getenv('SENDGRID_API_KEY')
        
        if not sg_api_key:
            print(f"📧 OTP for {recipient_email}: {otp}")
            return True
        
        message = Mail(
            from_email=os.getenv('EMAIL_USER', 'noreply@fitplan-ai.com'),
            to_emails=recipient_email,
            subject='FitPlan-AI - Your Verification Code',
            plain_text_content=f'Your verification code is: {otp}\n\nThis code expires in 10 minutes.'
        )
        
        sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
        response = sg.send(message)
        
        return response.status_code in [200, 202]
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
