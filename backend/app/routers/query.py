from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.llm_service import generate_answer

router = APIRouter()


class QueryRequest(BaseModel):
    document_id: str
    question: str
    top_k: int = 5


class Citation(BaseModel):
    page: int
    section: str
    clause_title: str
    excerpt: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]


@router.post("", response_model=QueryResponse)
async def ask_question(payload: QueryRequest):
    """
    Retrieves the most relevant clauses for the question, generates a
    grounded answer, and returns it alongside the citations that support it.
    """
    chunks = retrieve_relevant_chunks(
        document_id=payload.document_id,
        query=payload.question,
        top_k=payload.top_k,
    )
    result = generate_answer(question=payload.question, context_chunks=chunks)

    return QueryResponse(
        answer=result["answer"],
        citations=[
            Citation(
                page=c["page"],
                section=c["section"],
                clause_title=c["clause_title"],
                excerpt=c["excerpt"],
            )
            for c in result["citations"]
        ],
    )
