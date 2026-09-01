# LegalLens AI — AI-Powered Contract Intelligence Platform

> Upload a contract. Ask it anything. Get answers grounded in the exact clause and page they came from.

LegalLens AI is a Retrieval-Augmented Generation (RAG) platform that turns dense legal documents — employment contracts, NDAs, leases, purchase agreements — into something you can actually query, audit, and understand. It doesn't just summarize; it retrieves the specific clause behind every answer and cites it, so nothing is taken on faith.

![Status](https://img.shields.io/badge/status-in--development-yellow)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents

- [Why This Exists](#why-this-exists)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Evaluation](#evaluation)
- [Engineering Decisions](#engineering-decisions)
- [Roadmap](#roadmap)
- [Challenges & Learnings](#challenges--learnings)
- [Contributing](#contributing)
- [License](#license)

---

## Why This Exists

Most "chat with your PDF" RAG projects use fixed-size chunking and hand the model a wall of retrieved text with no way to verify it. That's fine for a demo, useless for a document where a single misread clause has real consequences.

LegalLens AI is built around one constraint: **every answer must be traceable back to a specific clause, section, and page.** That constraint shapes everything downstream — how documents are chunked, how retrieval is scored, and how answers are generated and displayed.

## Features

### Core (MVP)
- **Multi-format ingestion** — PDF, DOCX, and scanned images via OCR (Tesseract / PaddleOCR)
- **Structure-aware chunking** — splits by section/article/clause boundaries instead of fixed character windows
- **Semantic search** — sentence-transformer embeddings stored in FAISS / ChromaDB
- **Grounded Q&A** — every answer includes a citation: page number, section, and clause title
- **Ask Anything** — natural-language questions like *"Can the company terminate me without notice?"*

### Document Intelligence
| Feature | Description |
|---|---|
| **Risk Analysis** | Flags high-risk patterns: unlimited liability, one-sided indemnification, auto-renewal, jurisdiction issues |
| **Deadline Extraction** | Pulls out payment due dates, notice periods, renewal windows, contract end dates |
| **Key Clause Extraction** | Auto-locates confidentiality, termination, arbitration, governing law, liability, IP ownership clauses |
| **Plain-English Summaries** | Rewrites legal clauses at a "explain it to a college student" reading level |
| **Clause Comparison** | Diffs two contracts and reports what changed in termination, payment, and liability terms |
| **Contract Scoring** | Rule-based (not hand-waved) scores for overall risk, fairness, and complexity |
| **Red Flag Detection** | Missing signatures, unlimited liability, excessive penalties, missing governing law |
| **Contract Timeline** | Visual timeline from signing → payment → renewal → expiry |

## Architecture

```
                    ┌─────────────────┐
                    │  React Frontend │
                    └────────┬────────┘
                             │ REST / WebSocket
                    ┌────────▼────────┐
                    │  FastAPI Backend│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                     │
┌───────▼───────┐  ┌─────────▼────────┐  ┌─────────▼────────┐
│  OCR Pipeline  │  │  Clause Chunker  │  │  Deadline/Risk    │
│ (Tesseract/    │  │  (section-aware  │  │  Extraction        │
│  PaddleOCR)    │  │   splitter)      │  │  (rule + LLM)      │
└───────┬───────┘  └─────────┬────────┘  └─────────┬────────┘
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Embedding Model │  (bge-large-en / MiniLM)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  FAISS / Chroma │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Retriever     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │       LLM        │  (Ollama local / OpenAI API)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Answer + Citation│
                    └──────────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | FastAPI (Python 3.11) |
| Orchestration | LangChain |
| LLM | Ollama (local) / OpenAI API (optional) |
| Embeddings | Sentence-Transformers (`BAAI/bge-large-en` or `all-MiniLM-L6-v2`) |
| Vector Store | FAISS (dev) / ChromaDB (alt) |
| Relational DB | PostgreSQL — users, contract metadata, extracted deadlines, audit log |
| OCR | PaddleOCR / Tesseract |
| Deployment | Docker, Docker Compose, Render / Railway / Fly.io |

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (recommended)
- (Optional) An OpenAI API key, or Ollama installed locally for a fully offline setup

### Quick Start with Docker

```bash
git clone https://github.com/<your-username>/LegalLens-AI.git
cd LegalLens-AI
cp .env.example .env      # fill in your keys / config
docker compose -f docker/docker-compose.yml up --build
```

- Backend: `http://localhost:8000` (docs at `/docs`)
- Frontend: `http://localhost:5173`

### Manual Setup

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
LegalLens-AI/
├── frontend/               # React + TypeScript UI
│   └── src/
│       ├── components/     # Reusable UI components
│       ├── pages/          # Route-level views
│       ├── hooks/          # Custom React hooks
│       └── api/            # Backend API client
├── backend/
│   └── app/
│       ├── routers/        # FastAPI route handlers
│       ├── services/       # OCR, chunking, embedding, retrieval, LLM logic
│       ├── models/         # Pydantic + DB models
│       └── core/           # Config, DB session, settings
├── models/                 # Local model weights / cache (gitignored)
├── embeddings/             # Embedding generation scripts
├── vector_store/           # FAISS/Chroma index artifacts (gitignored)
├── contracts/samples/      # Sample contracts for testing/demo
├── tests/                  # Integration tests
├── docker/                 # Dockerfiles + docker-compose
├── screenshots/            # Demo screenshots for this README
└── requirements.txt
```

## Usage

1. Upload a contract (PDF, DOCX, or scanned image).
2. The system OCRs (if needed), chunks by clause/section, embeds, and indexes it.
3. Ask a question in plain English, or click a quick-action button (Risk Analysis, Deadlines, Key Clauses, Summarize).
4. Every answer returns with its source: **page, section, and clause title.**

**Example**

> **Q:** What happens if the client terminates early?
>
> **A:** The client may terminate with 30 days' written notice; no early-termination penalty applies.
>
> **Source:** Page 8 · Section 6.2 · Termination Clause

## Evaluation

Retrieval and generation are evaluated on a held-out set of annotated contract Q&A pairs using:
- **Retrieval:** Recall@k and MRR against manually labeled ground-truth clauses
- **Generation:** Faithfulness (is the answer supported by the retrieved clause?) and citation accuracy
- Results and methodology are tracked in [`tests/eval/`](tests/eval/) *(add results here once benchmarking is complete)*

## Engineering Decisions

Short write-ups worth having ready for interviews:

- **Why clause-based chunking over fixed-size windows** — legal meaning lives at the clause boundary; splitting mid-clause destroys retrieval precision.
- **Why citations are mandatory, not optional** — reduces hallucination risk and makes the system auditable, which matters for a legal use case.
- **Why `bge-large-en` (or MiniLM as a lighter alternative)** — trade-off between retrieval quality and inference cost/latency.
- **How OCR errors are handled** — confidence thresholds + fallback re-chunking when OCR output is low-confidence.
- **Deployment structure** — containerized services, environment-based config, health checks.

## Roadmap

- [ ] Core RAG pipeline (upload → OCR → chunk → embed → retrieve → answer + citation)
- [ ] Risk analysis + red flag detection
- [ ] Deadline extraction
- [ ] Clause comparison (Contract A vs Contract B)
- [ ] Contract scoring (risk / fairness / complexity)
- [ ] Contract timeline visualization
- [ ] Multi-user auth + saved document history
- [ ] Retrieval evaluation harness + published benchmark results

## Challenges & Learnings

*(Fill this in as you build — this section is often the most interesting part of the README to interviewers.)*

- Handling inconsistent contract formatting/numbering across document sources
- Balancing chunk granularity: too fine loses context, too coarse hurts citation precision
- OCR reliability on low-quality scans and its downstream effect on chunking

## Contributing

Contributions, issues, and feature requests are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) if present, or open an issue to discuss changes.

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
