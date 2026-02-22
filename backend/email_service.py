import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(recipient_email: str, subject: str, body: str, reply_to: str | None = None) -> dict:
    """
    Send email using Gmail SMTP.
    
    Args:
        recipient_email: Email address of the recipient
        subject: Email subject line
        body: Email body content
        reply_to: Optional reply-to email address
        
    Returns:
        dict: Status of email sending with 'success' boolean and 'message' string
    """
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        
        if not email_user or not email_pass:
            return {
                "success": False,
                "message": "Email credentials not configured. Please set EMAIL_USER and EMAIL_PASS environment variables."
            }
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = recipient_email
        msg['Subject'] = subject
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using SMTP_SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
        
        return {
            "success": True,
            "message": f"Email successfully sent to {recipient_email}"
        }
        
    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "message": "Authentication failed. Please check your email credentials."
        }
    except smtplib.SMTPRecipientsRefused:
        return {
            "success": False,
            "message": f"Invalid recipient email address: {recipient_email}"
        }
    except smtplib.SMTPException as e:
        return {
            "success": False,
            "message": f"SMTP error occurred: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }
