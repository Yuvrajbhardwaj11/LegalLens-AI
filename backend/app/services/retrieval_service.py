"""
Retrieves the top-k most relevant chunks for a question, scoped to a
specific document.
"""
import json
import os

import faiss
import numpy as np

from app.core.config import settings
from app.services.embedding_service import _get_model


def retrieve_relevant_chunks(document_id: str, query: str, top_k: int = 5) -> list[dict]:
    """
    Returns a list of chunk dicts:
        {"text": ..., "section": ..., "clause_title": ..., "page": ..., "score": ...}
    """
    index_path = os.path.join(settings.VECTOR_STORE_PATH, f"{document_id}.index")
    meta_path = os.path.join(settings.VECTOR_STORE_PATH, f"{document_id}.json")

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError(f"No indexed document found for document_id={document_id}")

    index = faiss.read_index(index_path)
    with open(meta_path) as f:
        metadata = json.load(f)
    chunks = metadata["chunks"]

    model = _get_model()
    query_vector = np.array(list(model.embed([query])), dtype="float32")
    faiss.normalize_L2(query_vector)

    top_k = min(top_k, index.ntotal)
    scores, indices = index.search(query_vector, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = chunks[idx]
        results.append({
            "text": chunk["text"],
            "section": chunk["section"],
            "clause_title": chunk["clause_title"],
            "page": chunk["page"],
            "score": float(score),
        })
    return results
