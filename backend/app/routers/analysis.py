from fastapi import APIRouter

from app.services.risk_service import analyze_risk
from app.services.deadline_service import extract_deadlines
from app.services.clause_service import extract_key_clauses, compare_documents

router = APIRouter()


@router.get("/{document_id}/risk")
async def get_risk_analysis(document_id: str):
    """Returns flagged high-risk clauses and an overall risk assessment."""
    return analyze_risk(document_id)


@router.get("/{document_id}/deadlines")
async def get_deadlines(document_id: str):
    """Returns extracted dates: payment due, notice period, renewal, expiry."""
    return extract_deadlines(document_id)


@router.get("/{document_id}/clauses")
async def get_key_clauses(document_id: str):
    """Returns located key clauses: confidentiality, termination, IP, etc."""
    return extract_key_clauses(document_id)


@router.post("/compare")
async def compare(document_id_a: str, document_id_b: str):
    """Diffs two contracts and reports differences in key clause categories."""
    return compare_documents(document_id_a, document_id_b)
