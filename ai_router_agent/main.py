# AI Router Agent
# Run locally --> python -m uvicorn main:app --port 8000
# Swagger URL --> http://127.0.0.1:8000/docs
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from router.router_agent import route
from services.email_service import call_email_agent
from services.teams_service import call_teams_agent
from services.weather_service import call_weather_agent
from utils.trace_id import generate_trace_id
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ================================
# APP SETUP
# ================================
app = FastAPI(title="AI Router Agent")

# ================================
# REQUEST / RESPONSE MODELS
# ================================
class RouterRequest(BaseModel):
    message: str
    auto_approve: bool = False  # optional human-in-the-loop flag

class RouterResponse(BaseModel):
    agent: str
    payload: dict
    status: str
    trace_id: str
    confidence_score: float = None

# ================================
# POST API ENDPOINT - /agent/execute
# ================================
@app.post("/agent/execute", response_model=RouterResponse)
def execute_agent(req: RouterRequest):
    trace_id = generate_trace_id()
    logger.info(f"[{trace_id}] Called API: /agent/execute")
    try:
        user_input = req.message
        logger.info(f"[{trace_id}] user_input={user_input}")

        # Step 1: Route the request using LLM
        decision = route(user_input, trace_id)
        logger.info(f"[{trace_id}] decision={decision}")
        agent_name = decision.get("agent")
        confidence_score = decision.get("confidence_score", 0.5)
        logger.info(f"[{trace_id}] agent_name={agent_name}, confidence_score={confidence_score}")
        agent_payload = decision.get("payload", {})

        # Step 2: Determine status based on confidence and auto_approve
        if confidence_score < 0.6:
            status = "NEEDS_REVIEW"
        elif req.auto_approve:
            status = "EXECUTED"
        else:
            status = "AWAITING_CONFIRMATION"

        # Step 3: Return early if not executing
        if status != "EXECUTED":
            return {
                "agent": agent_name,
                "payload": agent_payload,
                "status": status,
                "trace_id": trace_id,
                "confidence_score": confidence_score
            }

        # Step 4: Call the appropriate agent API
        if agent_name == "EMAIL_AGENT":
            result = call_email_agent({**agent_payload, "auto_approve": True}, trace_id)

        elif agent_name == "TEAMS_AGENT":
            result = call_teams_agent(agent_payload, trace_id)

        elif agent_name == "WEATHER_AGENT":
            result = call_weather_agent(agent_payload, trace_id)

        else:
            raise HTTPException(status_code=400, detail="Unknown agent")

        return {
            "agent": agent_name,
            "payload": result,
            "status": result.get("status", "EXECUTED"),
            "trace_id": trace_id,
            "confidence_score": confidence_score
        }

    except Exception as e:
        logger.error(f"[{trace_id}] Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
