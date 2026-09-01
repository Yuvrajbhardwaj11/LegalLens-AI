"""
Structure-aware chunking.

Unlike fixed-size chunking, this splits text along clause/section boundaries
so that each chunk is a semantically complete unit (e.g. "Section 6.2 —
Termination"). This is the single biggest lever on retrieval quality and
citation precision in this project.

Strategy:
    1. Try heuristic/regex detection of numbered sections & headers
       (e.g. "Section 5", "Article III", "6.2 Termination").
    2. If structure detection yields too few boundaries (inconsistent or
       unusual formatting), fall back to a semantic splitter that groups
       sentences by topic similarity instead of a fixed character count.
"""
import re
from dataclasses import dataclass

SECTION_HEADER_PATTERN = re.compile(
    r"^\s*(Section|Article|Clause)\s+([\dIVXLC]+)[\.\:]?\s*(.*)$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class Chunk:
    text: str
    section: str
    clause_title: str
    page: int


def chunk_document(text: str) -> list[Chunk]:
    boundaries = list(SECTION_HEADER_PATTERN.finditer(text))

    if len(boundaries) < 2:
        # Not enough structure detected — fall back to semantic chunking
        return _semantic_fallback_chunk(text)

    return _split_on_boundaries(text, boundaries)


def _split_on_boundaries(text: str, boundaries: list[re.Match]) -> list[Chunk]:
    chunks = []
    for i, match in enumerate(boundaries):
        start = match.start()
        end = boundaries[i + 1].start() if i + 1 < len(boundaries) else len(text)
        section_label = f"{match.group(1)} {match.group(2)}"
        clause_title = match.group(3).strip() or "Untitled"
        chunk_text = text[start:end].strip()

        # TODO: derive actual page number from page-offset tracking during extraction
        chunks.append(Chunk(text=chunk_text, section=section_label, clause_title=clause_title, page=0))

    return chunks


def _semantic_fallback_chunk(text: str) -> list[Chunk]:
    # TODO: sentence-level splitting + embedding-similarity grouping
    # (e.g. sliding window + cosine-similarity breakpoints, à la
    # semantic chunking approaches used in LangChain's SemanticChunker)
    raise NotImplementedError
