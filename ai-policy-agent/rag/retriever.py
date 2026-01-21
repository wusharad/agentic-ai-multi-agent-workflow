# Retrieve Relevant Policy Chunks (RAG Retriever)

import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity

from rag.loader import load_policy_documents
from rag.embedder import embed_documents, embedding_model
from utils.trace import get_trace_id
from utils.logging_utils import TraceLogger

base_logger = logging.getLogger(__name__)

# =====================================================
# RAG RETRIEVAL LOGIC
# =====================================================
def retrieve_policy_context(query: str, top_k: int = 3):
    """
    Retrieve relevant policy chunks using embedding similarity search.
    Trace-aware and logging enabled.
    """
    trace_id = get_trace_id()
    logger = TraceLogger(base_logger, {"trace_id": trace_id})

    logger.info("Starting policy context retrieval")
    logger.debug(f"Query received: {query}")

    # 1.Load policy documents
    documents = load_policy_documents()
    logger.info(f"Loaded {len(documents)} policy documents")

    if not documents:
        logger.warning("No policy documents found")
        return [], []

    doc_dicts = [
        {"source": source, "content": content}
        for source, content in documents
    ]

    # 2.Embed documents
    embedded_data = embed_documents(doc_dicts)
    logger.info("Policy documents embedded successfully")

    # 3.Embed query
    query_embedding = embedding_model.encode([query])
    logger.debug("Query embedding generated")

    # 4.Similarity calculation
    similarities = cosine_similarity(
        query_embedding,
        embedded_data["embeddings"]
    )[0]

    logger.debug(f"Similarity scores: {similarities}")

    # 5.Top-k selection
    top_indices = np.argsort(similarities)[::-1][:top_k]

    policy_chunks = [embedded_data["texts"][i] for i in top_indices]
    similarity_scores = [float(similarities[i]) for i in top_indices]

    logger.info(f"Retrieved top {len(policy_chunks)} policy chunks")
    logger.debug(f"Top similarity scores: {similarity_scores}")

    return policy_chunks, similarity_scores
