# 🤖 AI Router Agent

**ai-router-agent** is an intelligent routing system that understands natural language user requests and routes them to appropriate specialized agents (email agent, policy agent, etc.) based on intent classification.

This project demonstrates **multi-agent orchestration** and **intelligent request routing**.

---

## ✨ Key Features

- 🧠 **Intent Classification** — understands user requests and determines appropriate agent
- 🔀 **Smart Routing** — routes requests to email agent, policy agent, or other services
- 📨 **Email Agent Integration** — handles email-related requests
- 📋 **Policy Agent Integration** — manages policy and compliance queries
- 🌐 **REST API Interface** — FastAPI with auto-generated Swagger docs
- 🔐 **Secure Routing** — validates requests before forwarding

---

## 🧱 High-Level Architecture
```
User Request
↓
Router Agent (Intent Classification)
↓
Route Decision:
├── Email Agent → Email Operations
├── Policy Agent → Policy Queries
└── Weather Service → Weather Info
```

---

## 📁 Project Structure
```
ai_router_agent/
│
├── main.py                 # FastAPI application (entry point)
├── requirements.txt
│
├── router/
│   ├── router_agent.py     # Core routing logic
│   ├── router_prompt.py    # Intent classification prompts
│   └── __init__.py
│
├── services/
│   ├── email_service.py    # Email agent integration
│   ├── teams_service.py    # Teams service integration
│   ├── weather_service.py  # Weather service integration
│   └── __init__.py
│
└── utils/
    └── trace_id.py         # Request tracing utilities
```

---

## 🚀 Setup Instructions

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Application
```bash
python main.py
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

### Route Request
**POST /route**
```json
{
  "message": "Send email to john@company.com about meeting",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "agent": "email_agent",
  "confidence": 0.95,
  "action": "forward_to_email_agent",
  "trace_id": "req_12345"
}
```

---

## 🧠 Routing Logic

The router analyzes user input and routes to:

- **Email Agent** — "send email", "schedule email", "email reminder"
- **Policy Agent** — "company policy", "compliance", "guidelines"
- **Weather Service** — "weather", "forecast", "temperature"
- **Teams Service** — "teams meeting", "schedule call"

---

## 🧪 Example Requests

- "Send email to team about project update" → **Email Agent**
- "What's the company policy on remote work?" → **Policy Agent**
- "What's the weather like today?" → **Weather Service**
- "Schedule a Teams meeting for tomorrow" → **Teams Service**

---

## 🔒 Security Features

- Request validation before routing
- Trace ID for request tracking
- Secure agent communication
- Input sanitization

---

## 🚧 Future Enhancements

- Machine learning-based intent classification
- Dynamic agent registration
- Load balancing across agents
- Request queuing and retry logic
- Agent health monitoring

---

## 📜 License

This project is for **learning, demonstration, and portfolio use**.