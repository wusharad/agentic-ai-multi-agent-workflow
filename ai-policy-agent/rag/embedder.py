"""
This file is responsible for:
1. Chunking policy documents
2. Generating embeddings
3. Returning clean, reusable vectors

No DB here.
No search here.
Just text → numbers.
"""

from typing import List, Dict
import logging
from sentence_transformers import SentenceTransformer

from utils.trace import get_trace_id
from utils.logging_utils import TraceLogger


# =====================================================
# EMBEDDING MODEL SETUP
# =====================================================

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Load model once (important for performance)
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

base_logger = logging.getLogger(__name__)


# =====================================================
# TEXT CHUNKING
# =====================================================
def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """
    Splits text into overlapping chunks for better semantic processing.
    """
    trace_id = get_trace_id()
    logger = TraceLogger(base_logger, {"trace_id": trace_id})

    logger.debug(
        f"Chunking text (length={len(text)} chars, "
        f"chunk_size={chunk_size}, overlap={overlap})"
    )

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    logger.debug(f"Generated {len(chunks)} chunks from document")
    return chunks


# =====================================================
# DOCUMENT EMBEDDING
# =====================================================
def embed_documents(documents: List[Dict]) -> Dict:
    """
    Generates embeddings for all document chunks using SentenceTransformer model.
    """
    trace_id = get_trace_id()
    logger = TraceLogger(base_logger, {"trace_id": trace_id})

    logger.info(f"Embedding {len(documents)} documents")

    texts: List[str] = []
    metadatas: List[Dict] = []

    for doc in documents:
        source = doc.get("source", "unknown")
        content = doc.get("content", "")

        if not content:
            logger.warning(f"Skipping empty document: {source}")
            continue

        logger.debug(f"Chunking document source: {source}")
        chunks = chunk_text(content)

        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({"source": source})

    if not texts:
        logger.warning("No text chunks generated for embedding")
        return {
            "texts": [],
            "embeddings": [],
            "metadatas": []
        }

    logger.info(f"Generating embeddings for {len(texts)} chunks")
    logger.debug("Calling SentenceTransformer.encode()")

    try:
        embeddings = embedding_model.encode(texts).tolist()
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise

    logger.info("Embedding generation completed successfully")
    logger.debug(
        f"Embedding vector size: {len(embeddings[0]) if embeddings else 0}"
    )

    return {
        "texts": texts,
        "embeddings": embeddings,
        "metadatas": metadatas
    }
