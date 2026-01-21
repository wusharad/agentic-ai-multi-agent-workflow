# LLM routing logic
import json
import re
import subprocess
from router.router_prompt import ROUTER_PROMPT
import logging
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def call_llama(prompt: str, trace_id: str) -> str:
    logger.info(f"[{trace_id}] Function call_llama: called")
    """
    Calls Ollama LLM with the given prompt and returns raw output.
    """
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    logger.info(f"[{trace_id}] Function call_llama: result={result}")

    if result.returncode != 0:
        raise RuntimeError(f"Ollama error: {result.stderr}")

    return result.stdout


def route(user_input: str, trace_id: str) -> dict:
    logger.info(f"[{trace_id}] Function called: route")
    """
    Routes the user input to the correct agent by using LLM decision.
    Ensures output is a proper dict.
    """
    prompt = ROUTER_PROMPT.format(user_input=user_input)
    logger.info(f"[{trace_id}] prompt = {prompt}")
    response = call_llama(prompt, trace_id)

    logger.info(f"[{trace_id}] Route agent raw response:{response}")

    raw_output = response.strip()
    logger.info(f"[{trace_id}] raw_output = {raw_output}")
    # Extract JSON safely using regex
    match = re.search(r"\{[\s\S]*\}", raw_output)
    logger.info(f"[{trace_id}] match={match}")
    if not match:
        raise ValueError(f"No JSON found in LLM output:\n{raw_output}")

    json_str = match.group()
    logger.info(f"[{trace_id}] json_str={json_str}")
    try:
        result = json.loads(json_str)
        # Clamp confidence score
        if 'confidence_score' in result:
            result['confidence_score'] = max(0.0, min(result['confidence_score'], 1.0))
            logger.info(f"[{trace_id}] confidence_score={result['confidence_score']}")
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned:\n{json_str}") from e