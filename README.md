# 📬 Resumail — AI Job Application Assistant

> Upload your resume. Pick a job. Get a personalized email — sent in seconds.

🌐 **[Try it live →](https://resumail.onrender.com)**

---

## ✨ What it does

Resumail takes your resume and a job position, and uses AI to write a professional, personalized job application email — then sends it for you.

No copy-pasting. No generic templates. Just smart, tailored emails.

---

## 🚀 How it works

1. **Create an account** — verified with a 6-digit OTP sent to your email
2. **Log in** securely
3. **Upload your resume** (PDF) — parsed automatically
4. **Enter the job position** you're applying for
5. **AI writes the email** — personalized to your resume and the role
6. **Review & edit** before sending
7. **Send** — delivered straight to the employer
8. **View history** — every email you've sent, saved to your dashboard

---

## 🛠️ Built with

| Layer | Tech |
|-------|------|
| Backend | FastAPI (Python) |
| AI | Groq LLM API |
| Database | PostgreSQL |
| Auth | JWT + bcrypt + OTP |
| Email | Brevo API |
| Frontend | Jinja2 + Tailwind CSS |
| Deployment | Docker + Render |

---

## 🔐 Security

- Passwords hashed with bcrypt
- Sessions managed with HTTP-only JWT cookies
- Email verified with 6-digit OTP before account activation
- No fake accounts, no spam

---

## 🐳 Run locally with Docker

```bash
git clone https://github.com/GauriSharma-tech/Resumail.git
cd Resumail
```

Add your keys to `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:password@db:5432/jobapp_db
GROQ_API_KEY=your_groq_key
GROQ_MODEL=llama-3.3-70b-versatile
BREVO_API_KEY=your_brevo_key
BREVO_SENDER_EMAIL=youremail@gmail.com
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

`BREVO_SENDER_EMAIL` must be a sender address verified in Brevo. If it is unset,
the backend uses `EMAIL_USER` as the sender address.

Then start everything:

```bash
docker compose up --build
```

Visit **http://localhost:8000** ✅

---

## 📁 Project structure

```
backend/
├── main.py           # App routes & middleware
├── auth.py           # JWT & bcrypt logic
├── auth_routes.py    # Register, OTP, login, logout
├── database.py       # PostgreSQL connection
├── models.py         # Database models
├── service.py        # AI email generation
├── email_service.py  # Email sending via Brevo
└── templates/        # HTML pages
```

---

## 🌐 API Endpoints

| Method | Route | What it does |
|--------|-------|--------------|
| GET | `/` | Home (protected) |
| POST | `/register` | Create account + send OTP |
| POST | `/verify-otp` | Verify your email |
| POST | `/login` | Login + set session |
| POST | `/generate-email` | AI generates your email |
| POST | `/send-email` | Send + save to history |
| GET | `/history` | Your email dashboard |

---

Crafted with late nights & coffee ☕ by [Gauri Sharma](https://github.com/GauriSharma-here)