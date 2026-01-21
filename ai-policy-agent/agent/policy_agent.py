"""
Policy Agent Logic
Responsibilities:
1. Retrieve policy context using RAG
2. Build LLM prompt
3. Call Ollama (llama3)
4. Parse STRICT JSON output
5. Compute confidence_score
6. Use propagated trace_id for logging & response
7. Decide escalation (no email sending here)

No FastAPI / HTTP logic here.
Pure agent intelligence.
"""

import json
import subprocess
import logging
from agent.policy_prompt import POLICY_AGENT_PROMPT
from rag.retriever import retrieve_policy_context
from utils.confidence import calculate_confidence_score
from utils.json_utils import extract_json
from utils.trace import get_trace_id
from utils.logging_utils import TraceLogger

base_logger = logging.getLogger(__name__)

# =====================================================
# MAIN POLICY AGENT ENTRY
# =====================================================
def process_policy_request(user_input: str, auto_approve: bool) -> dict:
    trace_id = get_trace_id()
    logger = TraceLogger(base_logger, {"trace_id": trace_id})

    logger.info("Policy request processing started")
    logger.info(f"User input received")

    # 1️.Retrieve policy context (RAG)
    policy_chunks, similarity_scores = retrieve_policy_context(user_input)
    logger.info(f"Retrieved {len(policy_chunks)} policy chunks")
    logger.debug(f"Similarity scores: {similarity_scores}")

    policy_context = "\n".join(policy_chunks) if policy_chunks else ""

    if not policy_chunks:
        logger.warning("No relevant policy context found")
        return {
            "answer": "I could not find this information in the company policy.",
            "escalation_required": False,
            "department": None,
            "email_payload": None,
            "status": "NO_POLICY_FOUND",
            "trace_id": trace_id,
            "confidence_score": 0.0,
            "next_action": "no next action needed"
        }

    # 2️.Build LLM prompt
    logger.info("LLM prompt construction start!")
    prompt = POLICY_AGENT_PROMPT.replace("{policy_context}", policy_context).replace("{user_input}", user_input)
    logger.info("LLM prompt construction end!")

    # 3️.Call LLM
    llm_response = call_llama(prompt, logger)
    logger.info(f"Raw LLM output:\n{llm_response}")

    # 4️.Parse JSON
    try:
        data = extract_json(llm_response)
        logger.info("LLM JSON parsed successfully")
    except json.JSONDecodeError:
        logger.error("Invalid JSON returned by LLM")
        logger.debug(f"Raw LLM output: {llm_response}")
        raise ValueError("Invalid JSON returned by LLM")

    # 5️.Normalize fields
    answer = data.get("answer", "I could not find this information in the company policy.")
    escalation_required = bool(data.get("escalation_required", False))
    department = data.get("department", "NA")
    email_payload = data.get("email_payload", "NA")
    next_action = data.get("next_action", "no next action needed")

    # 6️.Compute confidence score
    confidence_score = calculate_confidence_score(similarity_scores)
    logger.info(f"Confidence score calculated: {confidence_score}")

    # 7️.Decide status (no email sending here)
    if confidence_score < 0.5:
        status = "LOW_CONFIDENCE"
    elif escalation_required and not auto_approve:
        status = "AWAITING_CONFIRMATION"
    elif escalation_required:
        status = "ESCALATION_REQUIRED"
    else:
        status = "ANSWERED"

    logger.info(f"Policy processing completed with status: {status}")

    return {
        "answer": answer,
        "escalation_required": escalation_required,
        "department": department,
        "email_payload": email_payload,
        "status": status,
        "trace_id": trace_id,
        "confidence_score": confidence_score,
        "next_action": next_action
    }


# =====================================================
# LLM CALL
# =====================================================
def call_llama(prompt: str, logger: logging.Logger) -> str:
    logger.info("Calling Ollama LLM")

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    if result.returncode != 0:
        logger.error(f"Ollama execution failed: {result.stderr}")
        raise RuntimeError("Ollama execution failed")

    logger.info("Ollama LLM call completed")
    return result.stdout.strip()
