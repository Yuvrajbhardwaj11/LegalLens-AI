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
       unusual formatting), fall back to a paragraph-based splitter with
       overlap, so we never fail to chunk a document outright.

Page tracking: ocr_service tags extracted text with `[[PAGE n]]` markers.
We strip those out here but use their positions to know which page each
chunk started on.
"""
import re
from dataclasses import dataclass

SECTION_HEADER_PATTERN = re.compile(
    r"^\s*(Section|Article|Clause)\s+([\dIVXLC]+)[\.\:]?\s*(.*)$",
    re.IGNORECASE | re.MULTILINE,
)
PAGE_MARKER_PATTERN = re.compile(r"\[\[PAGE (\d+)\]\]")


@dataclass
class Chunk:
    text: str
    section: str
    clause_title: str
    page: int


def chunk_document(text: str) -> list[Chunk]:
    page_map = _build_page_offset_map(text)
    clean_text = PAGE_MARKER_PATTERN.sub("", text)

    boundaries = list(SECTION_HEADER_PATTERN.finditer(clean_text))

    if len(boundaries) < 2:
        return _paragraph_fallback_chunk(text, page_map)

    return _split_on_boundaries(clean_text, boundaries, text, page_map)


def _build_page_offset_map(raw_text: str) -> list[tuple[int, int]]:
    """Returns [(offset_in_raw_text, page_number), ...] sorted by offset."""
    return [(m.start(), int(m.group(1))) for m in PAGE_MARKER_PATTERN.finditer(raw_text)]


def _page_for_offset(offset_in_clean_text: int, clean_text: str, raw_text: str, page_map: list[tuple[int, int]]) -> int:
    if not page_map:
        return 1
    # Approximate: map proportionally between clean and raw text lengths
    approx_raw_offset = int(offset_in_clean_text * (len(raw_text) / max(len(clean_text), 1)))
    page = 1
    for offset, page_num in page_map:
        if offset <= approx_raw_offset:
            page = page_num
        else:
            break
    return page


def _split_on_boundaries(clean_text: str, boundaries: list[re.Match], raw_text: str, page_map: list[tuple[int, int]]) -> list[Chunk]:
    chunks = []
    for i, match in enumerate(boundaries):
        start = match.start()
        end = boundaries[i + 1].start() if i + 1 < len(boundaries) else len(clean_text)
        section_label = f"{match.group(1)} {match.group(2)}"
        clause_title = match.group(3).strip() or "Untitled"
        chunk_text = clean_text[start:end].strip()
        page = _page_for_offset(start, clean_text, raw_text, page_map)

        chunks.append(Chunk(text=chunk_text, section=section_label, clause_title=clause_title, page=page))

    return chunks


def _paragraph_fallback_chunk(raw_text: str, page_map: list[tuple[int, int]], max_chars: int = 800) -> list[Chunk]:
    """
    No clear section structure detected — group paragraphs into chunks up
    to max_chars, keeping paragraphs intact rather than cutting mid-sentence.
    """
    clean_text = PAGE_MARKER_PATTERN.sub("", raw_text)
    paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]

    chunks = []
    buffer = ""
    buffer_start_offset = 0
    running_offset = 0

    for para in paragraphs:
        if buffer and len(buffer) + len(para) > max_chars:
            page = _page_for_offset(buffer_start_offset, clean_text, raw_text, page_map)
            chunks.append(Chunk(text=buffer.strip(), section=f"Part {len(chunks) + 1}", clause_title="Untitled", page=page))
            buffer = ""
            buffer_start_offset = running_offset

        if not buffer:
            buffer_start_offset = running_offset
        buffer += para + "\n\n"
        running_offset += len(para) + 2

    if buffer.strip():
        page = _page_for_offset(buffer_start_offset, clean_text, raw_text, page_map)
        chunks.append(Chunk(text=buffer.strip(), section=f"Part {len(chunks) + 1}", clause_title="Untitled", page=page))

    return chunks
