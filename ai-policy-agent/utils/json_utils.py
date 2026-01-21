import re
import json

def extract_json(llm_output: str) -> dict:
    """
    Extracts the FIRST valid JSON object from LLM output.
    """
    match = re.search(r"\{[\s\S]*\}", llm_output)
    if not match:
        raise ValueError("No JSON object found in LLM response")

    json_str = match.group()
    return json.loads(json_str)
