# Calls ai_teams_agent API
import requests

TEAMS_AGENT_URL = "http://localhost:8002/teams/execute"

def call_teams_agent(payload: dict, trace_id: str):
    print(f"[{trace_id}] Agent called: TEAMS_AGENT")
    try:
        # return requests.post(TEAMS_AGENT_URL, json=payload).json()
        # Temporary mock response until teams service is available
        return {
            "message_id": "teams-67890",
            "channel": "dummy-channel",
            "message": "Dummy Message sent successfully",
            "sent_at": "2026-01-13T11:30:00Z",
            "status": "SUCCESS"
        }
    except requests.exceptions.RequestException:
        return {"status": "ERROR", "result": "Teams service unavailable"}
