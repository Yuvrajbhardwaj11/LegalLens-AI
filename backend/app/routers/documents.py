from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.ocr_service import extract_text
from app.services.chunking_service import chunk_document
from app.services.embedding_service import embed_and_index

router = APIRouter()

SUPPORTED_TYPES = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".txt"}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a contract file (PDF, DOCX, or scanned image), extracts text
    (OCR if needed), chunks it by clause/section, embeds the chunks, and
    indexes them for retrieval.
    """
    suffix = "." + file.filename.rsplit(".", 1)[-1].lower()
    if suffix not in SUPPORTED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    raw_bytes = await file.read()

    text, ocr_used = extract_text(raw_bytes, suffix)
    chunks = chunk_document(text)
    document_id = embed_and_index(chunks, source_filename=file.filename)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "ocr_used": ocr_used,
        "num_chunks": len(chunks),
    }


@router.get("/{document_id}")
async def get_document(document_id: str):
    # TODO: fetch document metadata + chunk list from DB
    raise HTTPException(status_code=501, detail="Not implemented yet")
