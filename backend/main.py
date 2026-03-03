import io
import re
import time
from pathlib import Path

import pdfplumber
from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from backend.auth import decode_access_token
from backend.auth_routes import router as auth_router
from backend.database import engine, get_db
from backend.email_service import send_email
from backend.models import Base, EmailHistory
from backend.service import EmailGnerator

BASE_DIR = Path(__file__).resolve().parent

# Create tables on startup
Base.metadata.create_all(bind=engine)


def extract_email_from_resume(text: str) -> str | None:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone_from_resume(text: str) -> str | None:
    match = re.search(r"[\+]?\d[\d\s\-\(\)]{8,14}", text)
    return match.group(0).strip() if match else None


def extract_resume_text(file_bytes: bytes) -> str:
    resume_text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text.append(page_text)
    return "\n".join(resume_text)


app = FastAPI()

# CORS middleware allows frontend/API clients from other origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","https://resumail.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware logs method, path, and duration.
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)
        print(f"{request.method} {request.url.path} - {response.status_code} ({duration}ms)")
        return response


app.add_middleware(LoggingMiddleware)
app.include_router(auth_router)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Authentication middleware for protected routes.
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    protected_routes = ["/", "/generate-email", "/send-email", "/history"]

    if request.url.path in protected_routes:
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse(url="/login", status_code=302)

        payload = decode_access_token(token)
        if not payload:
            return RedirectResponse(url="/login", status_code=302)

    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-email", response_class=HTMLResponse)
async def generate_email(
    request: Request,
    resume_file: UploadFile = File(...),
    job_position: str = Form(...),
    recipient_email: str = Form(...),
):
    """Step 1: Extract resume, generate email, show preview for editing."""
    try:
        filename = (resume_file.filename or "").lower()
        if not filename.endswith(".pdf"):
            return templates.TemplateResponse(
                "preview.html",
                {
                    "request": request,
                    "error": "Invalid file type. Please upload a PDF file.",
                    "subject": "",
                    "body": "",
                    "recipient_email": recipient_email,
                    "applicant_email": "",
                    "job_position": job_position,
                },
            )

        file_bytes = await resume_file.read()

        try:
            # Run PDF parsing in a worker thread to avoid blocking the event loop.
            resume_text = await run_in_threadpool(extract_resume_text, file_bytes)
        except Exception as e:
            return templates.TemplateResponse(
                "preview.html",
                {
                    "request": request,
                    "error": f"Error reading PDF: {str(e)}",
                    "subject": "",
                    "body": "",
                    "recipient_email": recipient_email,
                    "applicant_email": "",
                    "job_position": job_position,
                },
            )

        if not resume_text.strip():
            return templates.TemplateResponse(
                "preview.html",
                {
                    "request": request,
                    "error": "Could not extract text from PDF.",
                    "subject": "",
                    "body": "",
                    "recipient_email": recipient_email,
                    "applicant_email": "",
                    "job_position": job_position,
                },
            )

        applicant_email = extract_email_from_resume(resume_text)
        applicant_phone = extract_phone_from_resume(resume_text)

        try:
            email_generator = EmailGnerator()
            # Run external AI request in a worker thread to keep app responsive.
            email_response = await run_in_threadpool(
                email_generator.generate_email_from_resume_text,
                resume_text,
                job_position,
                applicant_email,
                applicant_phone,
            )

            if email_response.get("status") != "success":
                return templates.TemplateResponse(
                    "preview.html",
                    {
                        "request": request,
                        "error": email_response.get("message", "Failed to generate email."),
                        "subject": "",
                        "body": "",
                        "recipient_email": recipient_email,
                        "applicant_email": applicant_email or "",
                        "job_position": job_position,
                    },
                )

            subject = email_response.get("subject", "")
            body = email_response.get("body", "")

        except Exception as e:
            return templates.TemplateResponse(
                "preview.html",
                {
                    "request": request,
                    "error": f"Error generating email: {str(e)}",
                    "subject": "",
                    "body": "",
                    "recipient_email": recipient_email,
                    "applicant_email": applicant_email or "",
                    "job_position": job_position,
                },
            )

        return templates.TemplateResponse(
            "preview.html",
            {
                "request": request,
                "error": None,
                "subject": subject,
                "body": body,
                "recipient_email": recipient_email,
                "applicant_email": applicant_email or "",
                "job_position": job_position,
            },
        )

    except Exception as e:
        return templates.TemplateResponse(
            "preview.html",
            {
                "request": request,
                "error": f"Unexpected error: {str(e)}",
                "subject": "",
                "body": "",
                "recipient_email": recipient_email,
                "applicant_email": "",
                "job_position": job_position,
            },
        )


@app.post("/send-email", response_class=HTMLResponse)
async def send_email_route(
    request: Request,
    subject: str = Form(...),
    body: str = Form(...),
    recipient_email: str = Form(...),
    applicant_email: str = Form(""),
    job_position: str = Form(...),
    db: Session = Depends(get_db),
):
    """Step 2: User edited the email and now sends it."""
    token = request.cookies.get("access_token")
    payload = decode_access_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    email_status = await run_in_threadpool(
        send_email,
        recipient_email,
        subject,
        body,
        applicant_email if applicant_email else None,
    )

    if email_status.get("success"):
        history = EmailHistory(
            user_id=int(user_id),
            recipient_email=recipient_email,
            job_position=job_position,
            subject=subject,
            body=body,
        )
        db.add(history)
        db.commit()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "error": None,
            "subject": subject,
            "body": body,
            "recipient_email": recipient_email,
            "email_status": email_status,
        },
    )


@app.get("/history", response_class=HTMLResponse)
async def email_history(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    payload = decode_access_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    history = (
        db.query(EmailHistory)
        .filter(EmailHistory.user_id == int(user_id))
        .order_by(EmailHistory.sent_at.desc())
        .all()
    )

    return templates.TemplateResponse("history.html", {"request": request, "history": history})
