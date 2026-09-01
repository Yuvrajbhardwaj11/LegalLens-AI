"""
Locates standard clause categories within a document, and diffs two
documents against each other on those same categories.
"""

KEY_CLAUSE_CATEGORIES = [
    "confidentiality",
    "termination",
    "arbitration",
    "governing_law",
    "liability",
    "payment",
    "force_majeure",
    "ip_ownership",
]


def extract_key_clauses(document_id: str) -> dict:
    """
    Returns: {category: {"section": str, "clause_title": str, "excerpt": str} | None, ...}
    """
    # TODO:
    #   1. Load document chunks for document_id
    #   2. For each category, retrieve top match via embedding similarity
    #      against a category description (same retrieval mechanism as Q&A)
    raise NotImplementedError


def compare_documents(document_id_a: str, document_id_b: str) -> dict:
    """
    Returns per-category differences between two contracts, e.g.:
        {
            "termination": {"a": "...", "b": "...", "differs": True},
            ...
        }
    """
    clauses_a = extract_key_clauses(document_id_a)
    clauses_b = extract_key_clauses(document_id_b)

    # TODO: for each category, compare excerpts (semantic diff, not just
    # string equality) and summarize what changed via an LLM call
    raise NotImplementedError
