# 🤖 AI Email Agent

**ai-email-agent** is a local, agentic AI system that understands natural-language email requests, extracts structured intent using a local LLM, and safely sends or schedules emails via Gmail SMTP — with **human-in-the-loop approval** and a **REST API interface**.

This project demonstrates **real-world agent design**, not just LLM prompting.

---

## ✨ Key Features

- 🧠 **Local LLM (Ollama + Llama 3)** — no cloud LLM dependency
- 📨 **Natural language → structured JSON extraction**
- ⏰ **Time-aware reasoning** (today, tomorrow, next Monday, etc.)
- 🌍 **Timezone-safe scheduling** (Asia/Kolkata)
- 📧 **Email sending via Gmail SMTP** (no Google Cloud billing)
- ⏳ **Email scheduling** using APScheduler
- 🧍 **Human-in-the-loop confirmation** (safe by default)
- 🌐 **FastAPI REST API** with auto-generated Swagger docs
- 🔐 **Deterministic execution** (LLM never performs side effects)

---

## 🧱 High-Level Architecture
Client (Swagger / Postman / UI / n8n)
↓
FastAPI
↓
Local LLM (Ollama)
↓
Structured JSON
↓
Agent Validation (timezone-aware)
↓
Human Confirmation
↓
Action:
├── SEND_NOW → SMTP
└── SCHEDULE → APScheduler → SMTP

---

## 📁 Project Structure
ai_email_agent/
│
├── main.py # FastAPI application (entry point)
├── requirements.txt
│
├── agent/
│ ├── agent.py # Core agent logic (LLM + validation)
│ ├── llm_prompt.py # Deterministic extraction prompt
│ ├── email_tool.py # Gmail SMTP email sender
│ ├── confirmation.py # Human confirmation logic
│ └── init.py

---

## ⚙️ Prerequisites

- Python **3.10+**
- Gmail account with **App Password enabled**
- Ollama installed locally

---

## 🚀 Setup Instructions

### 1️⃣ Install Ollama & LLM

```bash
ollama pull llama3
```
Test: 
```bash
ollama run llama3
```
---
### 2️⃣ Clone & Install Dependencies
```bash
pip install -r requirements.txt
```
**Required libraries include:**
- fastapi
- uvicorn
- apscheduler
- pytz
- google-free SMTP (smtplib)
- ollama (CLI)
---
### 3️⃣ Configure Gmail SMTP
1. Enable 2-Step Verification on Gmail 
2. Generate App Password 
3. Update agent/.env
````
GMAIL_EMAIL="your_email@gmail.com"
GMAIL_APP_PASSWORD="your_16_char_app_password"
````
⚠️ Never use your actual Gmail password.
---
### ▶️ Running the Application
```bash
uvicorn main:app --reload
```
OR
```bash
python -m uvicorn main:app --reload --port 8000
```
**API will be available at:**
````
http://127.0.0.1:8000
````
**Swagger UI:**
```
http://127.0.0.1:8000/docs
```
---
## 🔌 API Endpoints
### 1️⃣ Extract Email Intent (Safe Mode)
**POST /agent/email**
```
{
  "message": "Send email to ramesh@gmail.com tomorrow at 10am about sprint review",
  "auto_approve": false
}
```
**Response:**
```
{
  "status": "AWAITING_CONFIRMATION",
  "extracted_data": {
    "recipient_email": "ramesh@gmail.com",
    "subject": "Sprint Review Meeting",
    "body": "Sprint review meeting",
    "send_time": "2026-01-12T10:00:00",
    "action": "SCHEDULE"
  }
}
```
---
### 2️⃣ Confirm & Execute Action
**POST /agent/email/confirm**
```
{
  "extracted_data": { ... },
  "approve": true
}
```
**Response:**
```
{
  "status": "EMAIL_SCHEDULED"
}
```
---
## 🧠 Agent Design Principles
- LLM is used only for reasoning and extraction
- All side effects are deterministic
- Approval is denied by default
- Timezone consistency enforced
- Two-step confirmation for safety
---
## 🧪 Example Natural Language Inputs

- “Send email to ramesh@gmail.com
 saying hello”
- “Email john@company.com
 tomorrow at 9am about standup”
- “Schedule an email to HR next Monday regarding leave”
---
## 🔒 Safety & Best Practices
- No email is sent without explicit approval
- SMTP credentials should be stored securely (env vars in production)
- Scheduler jobs are in-memory (can be extended to DB job stores)
---
## 🧠 Short Explanation
> This project demonstrates an agentic AI pattern where an LLM extracts structured intent, but deterministic Python code controls execution.  
> Human approval is required before any real-world action.
---
## 🚧 Future Enhancements
- Persistent job store (SQLite / Redis)
- Authentication (API key / JWT)
- Email preview & edit before confirmation
- Dockerization
- UI frontend
- Multi-agent workflows
---
## 📜 License

This project is for **learning, demonstration, and portfolio use**.