from pathlib import Path
import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from database import get_db
from models import User
from email_service import send_email

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()
    
    # If user exists but is not verified, we can resend OTP. If verified, show error.
    if existing_user:
        if existing_user.is_verified:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Email already registered and verified."
            })
        else:
            user = existing_user
    else:
        hashed = hash_password(password)
        user = User(email=email, hashed_password=hashed)
        db.add(user)
        
    # Generate OTP
    otp_code = str(random.randint(100000, 999999))
    user.otp = otp_code
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.commit()
    db.refresh(user)
    
    # Send Email
    subject = "Verify your Resumail Account"
    body = f"Your verification code is: {otp_code}. It will expire in 10 minutes."
    send_email(recipient_email=email, subject=subject, body=body)
    
    return RedirectResponse(url=f"/verify-otp?email={email}", status_code=302)


@router.get("/verify-otp", response_class=HTMLResponse)
async def verify_otp_page(request: Request, email: str):
    return templates.TemplateResponse("verify.html", {"request": request, "email": email})

@router.post("/verify-otp")
async def verify_otp(
    request: Request,
    email: str = Form(...),
    otp: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return templates.TemplateResponse("verify.html", {
            "request": request,
            "email": email,
            "error": "User not found."
        })
        
    if user.is_verified:
        return RedirectResponse(url="/login", status_code=302)
        
    if user.otp != otp:
        return templates.TemplateResponse("verify.html", {
            "request": request,
            "email": email,
            "error": "Invalid OTP."
        })
        
    if not user.otp_expiry or user.otp_expiry < datetime.utcnow():
        return templates.TemplateResponse("verify.html", {
            "request": request,
            "email": email,
            "error": "OTP has expired. Please register again to get a new code."
        })
        
    # Success
    user.is_verified = 1
    user.otp = None
    user.otp_expiry = None
    db.commit()
    
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password"
        })
        
    if not user.is_verified:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Please verify your email first. Check your inbox for the OTP."
        })
    
    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response
