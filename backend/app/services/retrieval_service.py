"""
Retrieves the top-k most relevant chunks for a question, scoped to a
specific document.
"""


def retrieve_relevant_chunks(document_id: str, query: str, top_k: int = 5) -> list[dict]:
    """
    Returns a list of chunk dicts:
        {"text": ..., "section": ..., "clause_title": ..., "page": ..., "score": ...}
    """
    # TODO:
    #   1. Embed the query with the same model used at ingestion time
    #   2. Search the document's FAISS/Chroma namespace for top_k nearest neighbors
    #   3. Return chunks with similarity scores for downstream ranking/filtering
    raise NotImplementedError
