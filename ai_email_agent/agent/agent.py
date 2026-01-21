# extraction contract (JSON rules)
import json
from agent.llm_prompt import EMAIL_EXTRACTION_PROMPT
from agent.llm_client import call_llama
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def extract_email_data(user_input: str) -> dict:
    prompt = EMAIL_EXTRACTION_PROMPT.format(user_input=user_input)
    response = call_llama(prompt)

    # Parse JSON safely
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from LLM:\n{response}")

    validate_data(data)
    return data

# VALIDATION & DECISION LOGIC
def validate_data(data: dict):
    """
      Validates extracted data and decides SEND_NOW vs SCHEDULE
      based on timezone-aware datetime comparison.
      """

    if "send_time" in data and data["send_time"]:
        send_time = datetime.fromisoformat(data["send_time"])

        # Ensure send_time is timezone-aware
        if send_time.tzinfo is None:
            send_time = IST.localize(send_time)

        now = datetime.now(IST)

        if send_time <= now:
            data["action"] = "SEND_NOW"
        else:
            data["action"] = "SCHEDULE"

    else:
        # No send_time provided → send immediately
        data["action"] = "SEND_NOW"

        # Basic field validation
    required_fields = ["recipient_email", "subject", "body", "action"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")