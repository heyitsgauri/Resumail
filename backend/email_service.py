import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().with_name(".env"))

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL") or os.getenv("EMAIL_USER")

def send_email(recipient_email: str, subject: str, body: str, reply_to: str | None = None) -> dict:
    if not BREVO_API_KEY:
        return {"success": False, "message": "BREVO_API_KEY is not configured."}
    if not BREVO_SENDER_EMAIL:
        return {
            "success": False,
            "message": "BREVO_SENDER_EMAIL or EMAIL_USER is not configured.",
        }

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY,
    }
    payload = {
        "sender": {"name": "Resumail", "email": BREVO_SENDER_EMAIL},
        "to": [{"email": recipient_email}],
        "subject": subject,
        "textContent": body,
    }

    if reply_to:
        payload["replyTo"] = {"email": reply_to}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
    except requests.RequestException as exc:
        return {"success": False, "message": f"Brevo request failed: {exc}"}

    if response.status_code == 201:
        return {"success": True, "message": "Email accepted by Brevo."}
    return {
        "success": False,
        "message": f"Brevo returned HTTP {response.status_code}: {response.text}",
    }