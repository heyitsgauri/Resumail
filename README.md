# Resumail — AI Job Application Assistant

A full-stack AI-powered platform that generates personalized job application emails from your resume using Groq LLM, with JWT authentication, per-user email history, and Gmail SMTP delivery.

## 🎯 What It Does

1. **Register/Login** — secure JWT-based authentication
2. **Upload Resume** — PDF parsed and text extracted automatically
3. **AI Generation** — Groq LLM generates a personalized email based on your resume and job position
4. **Preview & Edit** — review and edit the generated email before sending
5. **Send** — email sent via Gmail SMTP with Reply-To set to your email from resume
6. **History** — every sent email saved to your personal dashboard

## ✨ Features

- 🤖 AI-powered email generation using Groq LLM
- 📄 PDF resume parsing with automatic contact extraction (email + phone)
- 📧 Gmail SMTP delivery with intelligent Reply-To routing
- 🔐 JWT authentication with bcrypt password hashing
- 🗄️ PostgreSQL database with per-user email history
- 🛡️ HTTP middleware for auth, request logging, and CORS
- ✏️ Two-step flow — generate then edit before sending
- 🎨 Responsive UI with Tailwind CSS and Jinja2 templates

## 🏗️ Architecture

- **Backend**: FastAPI with middleware (auth, logging, CORS)
- **Frontend**: Server-rendered Jinja2 templates + Tailwind CSS
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI**: Groq LLM API for email generation
- **Auth**: JWT tokens stored in HTTP-only cookies
- **Email**: Gmail SMTP with Reply-To header routing

## 📁 Project Structure

```
backend/
    ├── main.py              # FastAPI app, routes, middleware
    ├── auth.py              # JWT + bcrypt logic
    ├── auth_routes.py       # Register, login, logout routes
    ├── database.py          # PostgreSQL connection + session
    ├── models.py            # User and EmailHistory ORM models
    ├── schemas.py           # Pydantic schemas
    ├── service.py           # Groq AI email generation
    ├── email_service.py     # Gmail SMTP sending
    ├── requirements.txt     # Dependencies
    ├── .env                 # Environment variables (never commit)
    ├── .env.example         # Template for env variables
    └── templates/
        ├── index.html       # Home page / upload form
        ├── preview.html     # Edit email before sending
        ├── result.html      # Send status page
        ├── history.html     # Email history dashboard
        ├── login.html       # Login page
        └── register.html    # Register page
```

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/resumail.git
cd resumail/backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/jobapp_db
EMAIL_USER=your.email@gmail.com
EMAIL_PASS=your_gmail_app_password
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Gmail App Password setup:
1. Enable 2-Factor Authentication on your Google Account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a password for "Mail"
4. Use that 16-character password as `EMAIL_PASS`

#### Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Set up PostgreSQL

Create a database:
```sql
CREATE DATABASE jobapp_db;
```

Tables are created automatically on first run.

### 5. Run the application

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000`

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home page (protected) |
| GET | `/register` | Register page |
| POST | `/register` | Create account |
| GET | `/login` | Login page |
| POST | `/login` | Authenticate + set JWT cookie |
| GET | `/logout` | Clear session |
| POST | `/generate-email` | Extract resume + generate email |
| POST | `/send-email` | Send edited email + save to history |
| GET | `/history` | User email history dashboard |

## 🛠️ Tech Stack

`FastAPI` `PostgreSQL` `SQLAlchemy` `JWT` `bcrypt` `Groq API` `pdfplumber` `Jinja2` `Tailwind CSS` `Gmail SMTP`

## 📄 License

MIT