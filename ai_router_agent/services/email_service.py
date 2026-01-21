# Calls ai_email_agent API
import requests

EMAIL_AGENT_URL = "http://localhost:8001/email/execute"

def call_email_agent(payload: dict, trace_id: str):
    print(f"[{trace_id}] Agent called: EMAIL_AGENT")
    try:
        # return requests.post(EMAIL_AGENT_URL, json=payload).json()
        # Temporary mock response until email service is available
        return {
            "email_id": "email-12345",
            "recipient": "dummy.user@example.com",
            "subject": "dummy- email subject",
            "sent_at": "2026-01-13T11:30:00Z",
            "status": "SUCCESS"
        }
    except requests.exceptions.RequestException:
        return {"status": "ERROR", "result": "Email service unavailable"}
