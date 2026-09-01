"""
Handles text extraction from uploaded documents.

Native-text PDFs/DOCX are parsed directly. Scanned documents (or PDFs with
no extractable text layer) fall back to OCR.
"""
from app.core.config import settings


def extract_text(raw_bytes: bytes, suffix: str) -> tuple[str, bool]:
    """
    Extracts text from a document's raw bytes.

    Returns:
        (text, ocr_used) — the extracted text, and whether OCR was required.
    """
    if suffix == ".docx":
        return _extract_docx(raw_bytes), False

    if suffix == ".pdf":
        text = _extract_pdf_native(raw_bytes)
        if _looks_like_scanned(text):
            return _extract_pdf_ocr(raw_bytes), True
        return text, False

    if suffix in {".png", ".jpg", ".jpeg"}:
        return _extract_image_ocr(raw_bytes), True

    raise ValueError(f"Unsupported file type: {suffix}")


def _extract_docx(raw_bytes: bytes) -> str:
    # TODO: use python-docx to walk paragraphs (and tables) in order
    raise NotImplementedError


def _extract_pdf_native(raw_bytes: bytes) -> str:
    # TODO: use pypdf to extract the text layer, page by page (preserve page numbers)
    raise NotImplementedError


def _looks_like_scanned(text: str) -> bool:
    # Heuristic: very little extractable text relative to page count implies a scan
    return len(text.strip()) < 50


def _extract_pdf_ocr(raw_bytes: bytes) -> str:
    # TODO: pdf2image -> per-page image -> pytesseract / PaddleOCR
    # Track OCR confidence per page; low-confidence pages should be flagged
    # so the chunker can handle them more conservatively.
    raise NotImplementedError


def _extract_image_ocr(raw_bytes: bytes) -> str:
    # TODO: pytesseract.image_to_string (or PaddleOCR) on the raw image
    raise NotImplementedError
