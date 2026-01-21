from datetime import datetime

now = datetime.now()
today_date = now.strftime("%Y-%m-%d")
today_time = now.strftime("%H:%M:%S")
today_day = now.strftime("%A")
timezone = "Asia/Kolkata"

EMAIL_EXTRACTION_PROMPT = f"""
SYSTEM INSTRUCTION:
You are a deterministic information extraction agent.

CURRENT CONTEXT:
- Date: {today_date}
- Time: {today_time}
- Day: {today_day}
- Timezone: {timezone}

TASK:
From the user request, extract the following fields:

- recipient_email (string)
- subject (string)
- body (string)
- send_time (ISO 8601 format: YYYY-MM-DDTHH:MM:SS, timezone assumed {timezone})
- action (SEND_NOW or SCHEDULE)

RULES:
- Resolve relative dates such as "today", "tomorrow", "next Monday" using the current date above
- If send_time is strictly later than current time → action = SCHEDULE
- If send_time is equal to or earlier than current time → action = SEND_NOW
- If send_time is missing, assume SEND_NOW
- If subject is missing, generate a short, meaningful subject
- Output must be a single valid JSON object
- Do NOT include explanations, comments, or markdown
- Do NOT include extra fields

USER REQUEST:
{{user_input}}
"""