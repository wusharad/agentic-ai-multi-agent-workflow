# =====================================================
# Calculate confidence score
# =====================================================

import logging
from utils.trace import get_trace_id
from utils.logging_utils import TraceLogger

base_logger = logging.getLogger(__name__)


def calculate_confidence_score(similarity_scores: list[float]) -> float:
    """
    Calculate confidence score (0.0 - 1.0) based on RAG similarity scores.

    Strategy:
    - No retrieved context → very low confidence
    - Strong average similarity → high confidence
    - Penalize weak / sparse matches
    """
    trace_id = get_trace_id()
    logger = TraceLogger(base_logger, {"trace_id": trace_id})

    logger.info("Calculating confidence score")

    if not similarity_scores:
        logger.warning("No similarity scores provided - returning minimal confidence")
        return 0.1

    # Clamp values defensively
    scores = [max(0.0, min(1.0, s)) for s in similarity_scores]
    logger.debug(f"Clamped similarity scores: {scores}")

    avg_score = sum(scores) / len(scores)
    max_score = max(scores)

    logger.debug(f"Average similarity score: {avg_score}")
    logger.debug(f"Maximum similarity score: {max_score}")

    # Weighted confidence:
    # - 70% based on average relevance
    # - 30% based on best match
    confidence = (0.7 * avg_score) + (0.3 * max_score)

    confidence = round(confidence, 2)

    logger.info(f"Final confidence score calculated: {confidence}")

    return confidence
