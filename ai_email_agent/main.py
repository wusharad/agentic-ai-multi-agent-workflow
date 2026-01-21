# Run locally --> python -m uvicorn main:app --reload --port 8000
from agent.agent import extract_email_data
from agent.email_tool import send_email
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi import Body
from pydantic import BaseModel
import pytz

# ================================
# APP & SCHEDULER SETUP
# ================================
app = FastAPI(title="AI Email Agent")
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))
scheduler.start()

# ================================
# REQUEST / RESPONSE MODELS
# ================================
class EmailRequest(BaseModel):
    message: str
    auto_approve: bool = False

class AgentResponse(BaseModel):
    extracted_data: dict
    status: str

# ================================
# Helper function
# ================================
def schedule_email(data: dict):
    send_time = datetime.fromisoformat(data["send_time"])

    # Ensure timezone-aware
    if send_time.tzinfo is None:
        send_time = pytz.timezone("Asia/Kolkata").localize(send_time)

    scheduler.add_job(
        send_email,
        trigger=DateTrigger(run_date=send_time),
        args=[data["recipient_email"], data["subject"], data["body"]],
        id=f"email_{data['recipient_email']}_{send_time.timestamp()}",
        replace_existing=True
    )
    print(f"⏳ Email scheduled to {data['recipient_email']} at {send_time}")

# =========================================================
# POST API ENDPOINT - /agent/email
# =========================================================
@app.post("/agent/email", response_model=AgentResponse)
def handle_email(req: EmailRequest):
    try:
        data = extract_email_data(req.message)
        print("Agent Output:", data)

        # Human-in-the-loop control
        if not req.auto_approve:
            return {
                "extracted_data": data,
                "status": "AWAITING_CONFIRMATION"
            }

        if data["action"] == "SEND_NOW":
            send_email(
                to_email=data["recipient_email"],
                subject=data["subject"],
                body=data["body"]
            )
            return {
                "extracted_data": data,
                "status": "EMAIL_SENT"
            }

        else:
            schedule_email(data)
            return {
                "extracted_data": data,
                "status": "EMAIL_SCHEDULED"
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================================================
# POST API ENDPOINT - /agent/email/confirm
# =========================================================
@app.post("/agent/email/confirm")
def confirm_email_action(payload: dict = Body(...)):
    data = payload.get("extracted_data")
    approve = payload.get("approve", False)

    if not approve:
        return {"status": "CANCELLED_BY_USER"}

    if data["action"] == "SEND_NOW":
        send_email(
            to_email=data["recipient_email"],
            subject=data["subject"],
            body=data["body"]
        )
        return {"status": "EMAIL_SENT"}

    schedule_email(data)
    return {"status": "EMAIL_SCHEDULED"}