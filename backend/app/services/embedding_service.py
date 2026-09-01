"""
Embeds chunks and writes them into the vector store, keyed by document_id.
"""
import uuid

from app.core.config import settings
from app.services.chunking_service import Chunk

_model = None  # lazy-loaded sentence-transformer


def _get_model():
    global _model
    if _model is None:
        # TODO: from sentence_transformers import SentenceTransformer
        # _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        raise NotImplementedError
    return _model


def embed_and_index(chunks: list[Chunk], source_filename: str) -> str:
    """
    Embeds each chunk and writes it to the configured vector store
    (FAISS or ChromaDB), namespaced under a new document_id.
    """
    document_id = str(uuid.uuid4())

    # TODO:
    #   1. model = _get_model()
    #   2. vectors = model.encode([c.text for c in chunks])
    #   3. write (vectors, metadata) to FAISS/Chroma under `document_id`
    #      metadata per chunk: {section, clause_title, page, source_filename}
    #   4. persist index to settings.VECTOR_STORE_PATH

    return document_id
