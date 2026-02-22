# Resumail — AI Job Application Assistant

A full-stack AI-powered platform that generates personalized job application emails from your resume using Groq LLM, with JWT authentication, per-user email history, and transactional email delivery via Brevo API.

🌐 **Live Demo**: https://resumail.onrender.com

## 🎯 What It Does

1. **Register/Login** — secure JWT-based authentication
2. **Upload Resume** — PDF parsed and text extracted automatically
3. **AI Generation** — Groq LLM generates a personalized email based on your resume and job position
4. **Preview & Edit** — review and edit the generated email before sending
5. **Send** — email sent via Brevo API with Reply-To set to your email from resume
6. **History** — every sent email saved to your personal dashboard

## ✨ Features

- 🤖 AI-powered email generation using Groq LLM
- 📄 PDF resume parsing with automatic contact extraction (email + phone)
- 📧 Transactional email delivery via Brevo API with intelligent Reply-To routing
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
- **Email**: Brevo API for transactional email delivery
- **Deployment**: Render (with UptimeRobot for 24/7 uptime)

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
    ├── email_service.py     # Brevo API email sending
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
git clone https://github.com/GauriSharma-tech/Resumail.git
cd Resumail
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/jobapp_db
GROQ_API_KEY=your_groq_api_key
BREVO_API_KEY=your_brevo_api_key
SECRET_KEY=your_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Groq API Key:
1. Go to [console.groq.com](https://console.groq.com)
2. Create an API key

#### Brevo API Key:
1. Sign up at [brevo.com](https://brevo.com)
2. Go to Settings → API Keys → Generate a new API key

#### Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Set up PostgreSQL

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

`FastAPI` `PostgreSQL` `SQLAlchemy` `JWT` `bcrypt` `Groq API` `pdfplumber` `Jinja2` `Tailwind CSS` `Brevo API` `Render`

