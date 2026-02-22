from pydantic import BaseModel, EmailStr
from datetime import datetime

# Auth schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Email history schemas
class EmailHistoryItem(BaseModel):
    id: int
    recipient_email: str
    job_position: str
    subject: str
    body: str
    sent_at: datetime

    class Config:
        from_attributes = True