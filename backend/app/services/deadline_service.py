"""
Extracts date-bound obligations: payment due dates, notice periods,
renewal windows, and contract end dates.
"""


def extract_deadlines(document_id: str) -> dict:
    """
    Returns:
        {
            "payment_due": [...],
            "notice_period": [...],
            "renewal_window": [...],
            "contract_end": [...],
        }
    """
    # TODO:
    #   1. Load document chunks for document_id
    #   2. Regex/NER pass for dates + surrounding obligation keywords
    #      (e.g. spaCy's date entity recognition, or a dateparser pass)
    #   3. Classify each date by nearby keyword ("due", "notice", "renew", "expir")
    raise NotImplementedError
