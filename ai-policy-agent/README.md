# 🤖 AI Policy Agent

**ai-policy-agent** is a local, agentic AI system that answers company policy questions using **RAG (Retrieval-Augmented Generation)**, extracts structured responses using a local LLM, and routes escalation actions to appropriate departments — with **human-in-the-loop approval** and a **REST API interface**.

This project demonstrates **real-world agent design** for enterprise policy management, not just LLM prompting.

---

## ✨ Key Features

- 🧠 **Local LLM (Ollama + Llama 3)** — no cloud LLM dependency
- 📚 **RAG-powered policy retrieval** using ChromaDB vector database
- 🎯 **Structured JSON extraction** from natural language queries
- 🏢 **Multi-department policy support** (HR, Finance, IT)
- 📧 **Smart escalation routing** to appropriate departments
- 🔍 **Confidence scoring** for answer reliability
- 🧍 **Human-in-the-loop confirmation** for escalations
- 🌐 **FastAPI REST API** with auto-generated Swagger docs
- 📊 **Distributed tracing** with trace IDs for debugging
- 🔐 **Deterministic execution** (LLM never performs side effects)

---

## 🧱 High-Level Architecture
```
Client (Swagger / Postman / UI)
↓
FastAPI
↓
RAG System (ChromaDB + Embeddings)
↓
Local LLM (Ollama)
↓
Structured JSON + Confidence Score
↓
Agent Validation
↓
Human Confirmation (if escalation needed)
↓
Action:
├── ANSWER → Direct Response
└── ESCALATE → Department Routing
```

---

## 📁 Project Structure
```
ai-policy-agent/
│
├── main.py                 # FastAPI application (entry point)
├── requirements.txt
├── .env                    # Environment configuration
│
├── agent/
│   ├── policy_agent.py     # Core agent logic (RAG + LLM)
│   ├── policy_prompt.py    # Structured extraction prompt
│   └── __init__.py
│
├── api/
│   ├── policy_api.py       # FastAPI routes and models
│   └── __init__.py
│
├── data/                   # Company policy documents
│   ├── hr_policy.md        # HR policies (leave, WFH, etc.)
│   ├── finance_policy.md   # Finance policies (reimbursements)
│   └── it_policy.md        # IT policies (assets, security)
│
├── rag/
│   ├── embedder.py         # Text embedding generation
│   ├── loader.py           # Policy document loader
│   ├── retriever.py        # Vector similarity search
│   └── __init__.py
│
├── utils/
│   ├── confidence.py       # Confidence score calculation
│   ├── json_utils.py       # JSON parsing utilities
│   ├── trace.py            # Distributed tracing
│   └── __init__.py
│
├── logs/
│   ├── logger.py           # Logging configuration
│   └── __init__.py
│
└── middleware/
    ├── trace_middleware.py  # Request tracing middleware
    └── __init__.py
```

---

## ⚙️ Prerequisites

- Python **3.10+**
- Ollama installed locally
- ChromaDB for vector storage

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

### 2️⃣ Clone & Install Dependencies
```bash
pip install -r requirements.txt
```
**Required libraries include:**
- fastapi
- uvicorn
- chromadb
- sentence-transformers
- pydantic
- python-dotenv
- requests
- pytz

### 3️⃣ Configure Environment
Update `.env` file with your settings:
```env
EMAIL_AGENT_URL=http://localhost:8001/agent/email
COMPANY_DOMAIN=abcd.com
HR_EMAIL=hr@abcd.com
FINANCE_EMAIL=finance@abcd.com
IT_EMAIL=it@abcd.com
ADMIN_EMAIL=admin@abcd.com
```

### 4️⃣ Initialize Vector Database
The system will automatically:
- Load policy documents from `data/` folder
- Generate embeddings using sentence-transformers
- Store vectors in ChromaDB for fast retrieval

---

## ▶️ Running the Application
```bash
uvicorn main:app --reload --port 8000
```
OR
```bash
python -m uvicorn main:app --reload --port 8000
```

**API will be available at:**
```
http://127.0.0.1:8000
```
**Swagger UI:**
```
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### 1️⃣ Health Check
**GET /policy-agent/health**
```json
{
  "status": "UP",
  "agent": "AI_POLICY_AGENT",
  "trace_id": "abc123"
}
```

### 2️⃣ Ask Policy Question
**POST /policy-agent/ask**
```json
{
  "message": "How many paid leaves do I get per year?",
  "auto_approve": false
}
```

**Response:**
```json
{
  "answer": "All full-time employees are entitled to 20 paid leaves per calendar year. Leave balance resets every January.",
  "escalation_required": false,
  "department": null,
  "email_payload": null,
  "status": "ANSWERED",
  "trace_id": "abc123",
  "confidence_score": 0.95,
  "next_action": "no next action needed"
}
```

### 3️⃣ Escalation Example
**Request:**
```json
{
  "message": "My laptop reimbursement has been pending for 20 days",
  "auto_approve": false
}
```

**Response:**
```json
{
  "answer": "Your laptop reimbursement should be processed within 15 working days. Since it's been 20 days, this needs escalation.",
  "escalation_required": true,
  "department": "finance",
  "email_payload": {
    "to": "finance@abcd.com",
    "subject": "Delayed Laptop Reimbursement - Escalation Required",
    "body": "Employee reimbursement has exceeded the 15-day processing timeline."
  },
  "status": "AWAITING_CONFIRMATION",
  "trace_id": "def456",
  "confidence_score": 0.88,
  "next_action": "escalate to finance department"
}
```

---

## 🧠 Agent Design Principles

- **RAG-First**: Always retrieve relevant policy context before answering
- **Confidence-Aware**: Calculate confidence scores based on similarity matches
- **Deterministic**: LLM used only for reasoning, not side effects
- **Traceable**: Every request has a unique trace ID for debugging
- **Safe Escalation**: Human approval required before contacting departments
- **Multi-Department**: Routes escalations to appropriate teams (HR/Finance/IT)

---

## 🧪 Example Natural Language Inputs

- "How many sick leaves can I take?"
- "What's the laptop reimbursement limit?"
- "Can I work from home 3 days a week?"
- "My IT ticket hasn't been resolved in 5 days"
- "When do leave balances reset?"
- "What documents do I need for travel reimbursement?"

---

## 🔒 Safety & Best Practices

- No emails sent without explicit human approval
- Policy documents stored locally (no external API calls)
- Confidence thresholds prevent low-quality answers
- Structured JSON prevents prompt injection
- Trace IDs enable full request debugging

---

## 📊 Response Status Types

- **ANSWERED**: Direct policy answer with high confidence
- **AWAITING_CONFIRMATION**: Escalation needed, waiting for approval
- **ESCALATION_REQUIRED**: Auto-approved escalation ready to execute
- **LOW_CONFIDENCE**: Answer found but confidence below threshold
- **NO_POLICY_FOUND**: No relevant policy information available

---

## 🧠 Short Explanation

> This project demonstrates an enterprise-grade agentic AI pattern where RAG retrieves relevant policy context, an LLM extracts structured intent, and deterministic Python code controls escalation workflows. Human approval ensures safe department routing.

---

## 🚧 Future Enhancements

- **Multi-language support** for global companies
- **Policy versioning** and change tracking
- **Advanced analytics** on common policy questions
- **Integration with HRMS/ERP systems**
- **Voice interface** for hands-free queries
- **Policy document auto-updates** from SharePoint/Confluence
- **Slack/Teams bot integration**
- **Role-based access control**

---

## 📜 License

This project is for **learning, demonstration, and portfolio use**.