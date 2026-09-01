"""
Rule-based + LLM-assisted risk flagging.

Kept rule-based where possible (e.g. presence/absence of a liability cap,
auto-renewal language) so risk scores are explainable rather than an opaque
LLM confidence number.
"""

RISK_PATTERNS = {
    "unlimited_liability": [r"unlimited liability", r"no limitation of liability"],
    "one_sided_indemnification": [r"indemnif(y|ication).{0,80}sole discretion"],
    "auto_renewal": [r"automatically renew", r"auto-renew"],
    "jurisdiction_issue": [r"exclusive jurisdiction", r"waives? right to jury trial"],
}


def analyze_risk(document_id: str) -> dict:
    """
    Returns:
        {
            "overall_risk_score": float,   # 0-10, derived from flag count/severity
            "flags": [{"type": str, "clause": str, "excerpt": str, "severity": str}, ...]
        }
    """
    # TODO:
    #   1. Load document chunks for document_id
    #   2. Run RISK_PATTERNS against chunk text (regex first pass)
    #   3. Optionally confirm/expand ambiguous matches with an LLM call
    #   4. Aggregate into an explainable score (e.g. weighted flag count)
    raise NotImplementedError
