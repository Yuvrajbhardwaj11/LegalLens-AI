"""
Generates a grounded answer from retrieved chunks and formats citations.

Design choice: the prompt instructs the model to answer ONLY from the
provided context and to explicitly reference which chunk(s) it used. This,
combined with returning the source chunk metadata alongside the answer,
is what keeps answers auditable instead of a black box.
"""
from app.core.config import settings

SYSTEM_PROMPT = """You are a contract analysis assistant. Answer the user's \
question using ONLY the provided contract excerpts. If the excerpts don't \
contain enough information to answer, say so explicitly — do not guess or \
use outside knowledge. Keep answers concise and in plain English."""


def generate_answer(question: str, context_chunks: list[dict]) -> dict:
    """
    Returns:
        {
            "answer": str,
            "citations": [
                {"page": int, "section": str, "clause_title": str, "excerpt": str},
                ...
            ]
        }
    """
    context_block = "\n\n".join(
        f"[{c['section']} — {c['clause_title']}, page {c['page']}]\n{c['text']}"
        for c in context_chunks
    )

    # TODO: call the configured LLM provider (Ollama or OpenAI) with
    # SYSTEM_PROMPT + context_block + question, per settings.LLM_PROVIDER
    raise NotImplementedError
