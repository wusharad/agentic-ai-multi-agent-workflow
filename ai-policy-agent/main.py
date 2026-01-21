# Entry point for AI Policy Agent
# Run using:
#   python -m uvicorn main:app --port 8000
# Swagger:
#   http://127.0.0.1:8000/docs

from fastapi import FastAPI
from api.policy_api import router as policy_router
from logs.logger import setup_logger
from middleware.trace_middleware import trace_middleware

# Initialize logging once for the whole app
setup_logger()

# ================================
# APP SETUP
# ================================
app = FastAPI(
    title="AI Policy Agent",
    description="Answers company policy questions using RAG and routes escalation actions if needed",
    version="1.0.0"
)

# Global middleware
app.middleware("http")(trace_middleware)

# Register APIs
app.include_router(policy_router)
