"""
Embeds chunks and writes them into a per-document FAISS index on disk,
alongside a metadata JSON file that maps vector positions back to
{section, clause_title, page, text}.

Uses fastembed (ONNX runtime, no PyTorch) instead of sentence-transformers
directly — same model quality, a fraction of the memory footprint, which
matters on free-tier hosts with limited RAM.
"""
import json
import os
import uuid

import faiss
import numpy as np
from fastembed import TextEmbedding

from app.core.config import settings
from app.services.chunking_service import Chunk

_model: TextEmbedding | None = None


def _get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=settings.EMBEDDING_MODEL)
    return _model


def embed_and_index(chunks: list[Chunk], source_filename: str) -> str:
    """
    Embeds each chunk and writes it to a FAISS index namespaced under a
    new document_id, plus a metadata sidecar file.
    """
    document_id = str(uuid.uuid4())
    os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)

    model = _get_model()
    texts = [c.text for c in chunks]
    vectors = np.array(list(model.embed(texts)), dtype="float32")
    faiss.normalize_L2(vectors)  # so inner product == cosine similarity

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, os.path.join(settings.VECTOR_STORE_PATH, f"{document_id}.index"))

    metadata = {
        "document_id": document_id,
        "source_filename": source_filename,
        "chunks": [
            {"text": c.text, "section": c.section, "clause_title": c.clause_title, "page": c.page}
            for c in chunks
        ],
    }
    with open(os.path.join(settings.VECTOR_STORE_PATH, f"{document_id}.json"), "w") as f:
        json.dump(metadata, f)

    return document_id
