import os
import logging
from typing import List, Tuple

from utils.trace import get_trace_id
from utils.logging_utils import TraceLogger

POLICY_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

base_logger = logging.getLogger(__name__)


def load_policy_documents() -> List[Tuple[str, str]]:
    """
    Loads all policy markdown files.

    Returns:
        List of tuples: (source_name, content)
    """
    trace_id = get_trace_id()
    logger = TraceLogger(base_logger, {"trace_id": trace_id})

    logger.info("Loading policy documents from data directory")
    logger.debug(f"Policy data directory path: {POLICY_DATA_DIR}")

    documents: List[Tuple[str, str]] = []

    if not os.path.exists(POLICY_DATA_DIR):
        logger.error("Policy data directory not found")
        raise FileNotFoundError(f"Policy data directory not found: {POLICY_DATA_DIR}")

    for filename in os.listdir(POLICY_DATA_DIR):
        if not filename.endswith(".md"):
            logger.debug(f"Skipping non-policy file: {filename}")
            continue

        file_path = os.path.join(POLICY_DATA_DIR, filename)
        logger.debug(f"Reading policy file: {filename}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

                if content:
                    documents.append((filename, content))
                    logger.debug(
                        f"Loaded policy file '{filename}' "
                        f"({len(content)} characters)"
                    )
                else:
                    logger.warning(f"Policy file '{filename}' is empty")

        except Exception as e:
            logger.error(f"Failed to read policy file '{filename}': {e}")
            raise

    if not documents:
        logger.warning("No policy documents found after scanning directory")
        raise ValueError("No policy documents found")

    logger.info(f"Successfully loaded {len(documents)} policy documents")

    return documents
