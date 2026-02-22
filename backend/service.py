import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class EmailGnerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing in environment")

        # Keep timeout bounded so requests fail fast instead of hanging.
        self.client = Groq(api_key=api_key, timeout=20, max_retries=1)

    def generate_email_from_resume_text(
        self,
        resume_text: str,
        job_position: str,
        applicant_email: str | None = None,
        applicant_phone: str | None = None
    ):
        """Generate professional job application from resume text"""

        # Build contact line dynamically from extracted info
        contact_lines = []
        if applicant_email:
            contact_lines.append(f"Email: {applicant_email}")
        if applicant_phone:
            contact_lines.append(f"Phone: {applicant_phone}")
        contact_block = "\n".join(contact_lines) if contact_lines else ""

        trimmed_resume = resume_text[:12000]

        prompt = f"""
        Based on the following resume, generate a professional job application email for the {job_position} position.

        Resume Content:
        {trimmed_resume}

        Generate a plain text email (NO markdown, NO formatting) with:
        - Professional subject line
        - Formal greeting (Dear Hiring Manager,)
        - Brief introduction expressing interest in the position
        - Summary of key qualifications and experience
        - Why you're a good fit for the role
        - Professional closing requesting an interview
        - Sign off exactly like this at the end:

        Best regards,
        [Candidate Name from resume]
        {contact_block}

        Write in first person as the job applicant.
        Use proper line breaks and paragraphs for readability.
        Do NOT use any markdown formatting like *, **, #, etc.

        Return ONLY a JSON object in this exact format:
        {{"subject": "your subject line", "email-body": "your plain text email content"}}
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="groq/compound-mini",
            )
            email_content = response.choices[0].message.content
            try:
                email_data = json.loads(email_content)
                return {
                    "subject": email_data.get("subject", ""),
                    "body": email_data.get("email-body", ""),
                    "status": "success"
                }
            except json.JSONDecodeError:
                return {
                    "subject": "",
                    "body": email_content,
                    "status": "success"
                }
        except Exception as e:
            return {
                "subject": "",
                "body": "",
                "status": "error",
                "message": f"Error generating email: {str(e)}"
            }
