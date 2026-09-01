"""
Generates a grounded answer from retrieved chunks and formats citations.

Design choice: the prompt instructs the model to answer ONLY from the
provided context. Combined with returning the source chunk metadata
alongside the answer, this is what keeps answers auditable instead of a
black box.

Provider: Groq's free API (OpenAI-compatible /chat/completions endpoint)
by default — fast, no-cost tier, runs open models like Llama 3.1/3.3.
Set LLM_PROVIDER=openai in .env to use OpenAI instead.
"""
import requests

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
    if not context_chunks:
        return {
            "answer": "I couldn't find any relevant clauses in this document to answer that question.",
            "citations": [],
        }

    context_block = "\n\n".join(
        f"[{c['section']} — {c['clause_title']}, page {c['page']}]\n{c['text']}"
        for c in context_chunks
    )

    user_prompt = f"Contract excerpts:\n\n{context_block}\n\nQuestion: {question}"

    if settings.LLM_PROVIDER == "groq":
        answer_text = _call_groq(user_prompt)
    elif settings.LLM_PROVIDER == "openai":
        answer_text = _call_openai(user_prompt)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")

    citations = [
        {
            "page": c["page"],
            "section": c["section"],
            "clause_title": c["clause_title"],
            "excerpt": c["text"][:200],
        }
        for c in context_chunks
    ]

    return {"answer": answer_text, "citations": citations}


def _call_groq(user_prompt: str) -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
        json={
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _call_openai(user_prompt: str) -> str:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
        json={
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
