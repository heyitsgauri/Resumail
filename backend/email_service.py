import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

def send_email(recipient_email: str, subject: str, body: str, reply_to: str | None = None) -> dict:
    try:
        url = "https://api.brevo.com/v3/smtp/email"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": BREVO_API_KEY
        }
        
        payload = {
            "sender": {"name": "Resumail", "email": "gaurisharma90043@gmail.com"},
            "to": [{"email": recipient_email}],
            "subject": subject,
            "textContent": body
        }
        
        if reply_to:
            payload["replyTo"] = {"email": reply_to}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            return {"success": True, "message": f"Email successfully sent to {recipient_email}"}
        else:
            return {"success": False, "message": f"Failed to send email: {response.text}"}
            
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {str(e)}"}