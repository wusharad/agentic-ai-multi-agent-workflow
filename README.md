# 🤖 Agentic AI Multi-Agent Workflow

**agentic-ai-multi-agent-workflow** is a comprehensive multi-agent AI system that demonstrates intelligent request routing, email automation, and policy management using local LLMs. This project showcases **real-world agent orchestration** with human-in-the-loop safety controls.

---

## 🌟 System Overview

This repository contains three specialized AI agents working together:

- **🔀 Router Agent** — Intelligent request routing and intent classification
- **📧 Email Agent** — Natural language email automation with scheduling
- **📋 Policy Agent** — RAG-powered company policy Q&A with escalation

---

## ✨ Key Features

- 🧠 **Local LLM Integration** (Ollama + Llama 3) — no cloud dependencies
- 🔀 **Multi-Agent Orchestration** — intelligent routing between specialized agents
- 📨 **Email Automation** — natural language to structured email actions
- 📚 **RAG-Powered Policy System** — ChromaDB vector search with confidence scoring
- ⏰ **Time-Aware Scheduling** — timezone-safe email scheduling
- 🧍 **Human-in-the-Loop Safety** — approval required for all actions
- 🌐 **REST API Architecture** — FastAPI with auto-generated Swagger docs
- 📊 **Distributed Tracing** — request tracking across all agents
- 🔐 **Secure by Design** — deterministic execution with LLM isolation

---

## 🧱 High-Level Architecture

```
User Request
↓
🔀 Router Agent (Intent Classification)
↓
Route Decision:
├── 📧 Email Agent → Email Operations (Send/Schedule)
├── 📋 Policy Agent → Policy Q&A + Escalation
└── 🌤️ Weather Service → Weather Information
```

---

## 📁 Repository Structure

```
agentic-ai-multi-agent-workflow/
│
├── 🔀 ai_router_agent/          # Intelligent request routing
│   ├── router/                  # Core routing logic
│   ├── services/                # Agent integrations
│   └── utils/                   # Tracing utilities
│
├── 📧 ai_email_agent/           # Email automation system
│   ├── agent/                   # Email agent logic
│   └── main.py                  # FastAPI application
│
├── 📋 ai-policy-agent/          # Policy management system
│   ├── agent/                   # Policy agent logic
│   ├── rag/                     # RAG implementation
│   ├── data/                    # Policy documents
│   └── api/                     # REST API endpoints
│
├── README.md                    # This file
└── LICENSE
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Ollama installed locally
- Gmail account with App Password (for email agent)

### 1️⃣ Install Ollama & LLM
```bash
ollama pull llama3
ollama run llama3  # Test installation
```

### 2️⃣ Setup Each Agent

#### Router Agent (Port 8000)
```bash
cd ai_router_agent
pip install -r requirements.txt
python main.py
```

#### Email Agent (Port 8001)
```bash
cd ai_email_agent
pip install -r requirements.txt
# Configure .env with Gmail credentials
python main.py
```

#### Policy Agent (Port 8002)
```bash
cd ai-policy-agent
pip install -r requirements.txt
# Configure .env with department emails
python main.py
```

### 3️⃣ Access APIs
- **Router Agent**: http://127.0.0.1:8000/docs
- **Email Agent**: http://127.0.0.1:8001/docs  
- **Policy Agent**: http://127.0.0.1:8002/docs

---

## 🔌 Multi-Agent Workflow Examples

### Email Automation Flow
```json
POST /route
{
  "message": "Send email to john@company.com tomorrow at 10am about sprint review",
  "user_id": "user123"
}
```
**Router Response:**
```json
{
  "agent": "email_agent",
  "action": "forward_to_email_agent",
  "confidence": 0.95
}
```

### Policy Query Flow
```json
POST /route
{
  "message": "How many paid leaves do I get per year?",
  "user_id": "user123"
}
```
**Router Response:**
```json
{
  "agent": "policy_agent",
  "action": "forward_to_policy_agent",
  "confidence": 0.92
}
```

---

## 🧠 Agent Capabilities

### 🔀 Router Agent
- Intent classification using natural language
- Confidence-based routing decisions
- Support for email, policy, weather, and Teams services
- Request validation and tracing

### 📧 Email Agent
- Natural language → structured email extraction
- Time-aware scheduling (today, tomorrow, next Monday)
- Timezone-safe operations (Asia/Kolkata)
- Gmail SMTP integration with App Passwords
- Human confirmation for all email actions

### 📋 Policy Agent
- RAG-powered policy retrieval using ChromaDB
- Multi-department support (HR, Finance, IT)
- Confidence scoring for answer reliability
- Smart escalation routing to appropriate departments
- Human approval for escalation emails

---

## 🧪 Example Natural Language Inputs

### Email Requests
- "Send email to team@company.com about project update"
- "Schedule reminder to john@company.com tomorrow at 9am"
- "Email HR next Monday regarding leave application"

### Policy Queries
- "What's the company policy on remote work?"
- "How many sick leaves can I take?"
- "My laptop reimbursement is delayed by 20 days"

### General Requests
- "What's the weather like today?"
- "Schedule a Teams meeting for tomorrow"

---

## 🔒 Safety & Security Features

- **Human-in-the-Loop**: All actions require explicit approval
- **Deterministic Execution**: LLMs used only for reasoning, not side effects
- **Request Validation**: Input sanitization and validation
- **Secure Credentials**: Environment-based configuration
- **Distributed Tracing**: Full request tracking with trace IDs
- **Confidence Thresholds**: Prevent low-quality responses

---

## 🛠️ Technology Stack

- **Framework**: FastAPI with auto-generated OpenAPI docs
- **LLM**: Ollama + Llama 3 (local deployment)
- **Vector DB**: ChromaDB for RAG implementation
- **Embeddings**: sentence-transformers
- **Scheduling**: APScheduler for email scheduling
- **Email**: Gmail SMTP with App Passwords
- **Tracing**: Custom distributed tracing system
- **Validation**: Pydantic models for type safety

---

## 🚧 Future Enhancements

### System-Wide
- Docker containerization for easy deployment
- Kubernetes orchestration for scalability
- Authentication & authorization (JWT/OAuth)
- Message queuing for async processing
- Agent health monitoring and auto-recovery

### Agent-Specific
- Machine learning-based intent classification
- Multi-language support for global deployment
- Integration with enterprise systems (HRMS, CRM)
- Voice interface for hands-free operation
- Advanced analytics and reporting dashboard

---

## 📊 Performance & Monitoring

- Request tracing across all agents
- Confidence score tracking
- Response time monitoring
- Error rate analysis
- Agent availability status

---

## 🤝 Contributing

This project demonstrates enterprise-grade agentic AI patterns. Contributions welcome for:
- New agent implementations
- Enhanced routing algorithms
- Additional service integrations
- Performance optimizations
- Security improvements

---

## 📜 License

This project is for **learning, demonstration, and portfolio use**.

---

## 🎯 Learning Outcomes

This repository demonstrates:
- Multi-agent system architecture
- Local LLM integration and orchestration  
- RAG implementation with vector databases
- Human-in-the-loop safety patterns
- REST API design for AI agents
- Distributed tracing and monitoring
- Real-world AI agent deployment patterns