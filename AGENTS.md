# AGENTS.md

> Context for OpenCode and AI coding assistants.

---

## Project Overview

**Name:** wikipdf — Wikipedia PDF Generator
**Type:** Python CLI tool
**Purpose:** Fetch Wikipedia articles and convert to PDF for offline reading

---

## Tech Stack

Python 3.12, fpdf2, wikipedia-api, click, requests-cache
pytest, pytest-mock, ruff, mypy

---

## Project Structure

```
pdf-scraping-rag/
├── src/wikipdf/           # Main package
│   ├── __init__.py
│   ├── __main__.py       # Entry: python -m wikipdf
│   ├── config.py        # Settings
│   ├── fetcher.py      # Wikipedia API
│   ├── pdfgen.py       # PDF generation
│   └── cli.py         # CLI commands
├── tests/               # Unit tests
├── output/               # Generated PDFs (gitignored)
└── requirements.txt
```

---

## Commands

### Development

```bash
pip install -r requirements.txt    # Install deps
ruff check .                      # Lint
ruff format .                    # Format
mypy src/                        # Type check
pytest                           # Run tests
pytest tests/test_fetcher.py      # Single test file
```

### Usage

```bash
python -m wikipdf fetch "Python (programming language)"      # Single article
python -m wikipdf fetch "Machine learning" -o ./output/       # Custom output dir
python -m wikipdf bulk topics.txt                           # Batch from file
python -m wikipdf bulk topics.txt -o ./output/             # Batch with output dir
python -m wikipdf --help
```

### Topics File Format

One topic per line. Blank lines and lines starting with `#` are ignored:

```
# My topics
Python_(programming_language)
Machine_learning
Deep_learning
```

---

## Error Handling

- Missing articles: Logs to `output/wikipdf_errors.log`
- Successful: Logs to `output/success.txt`

---

## Naming Convention

- Input: "Python (programming language)"
- Filename: `Python_(programming_language).pdf`
- Display in PDF: "Python (programming language)"

---

## Key Entry Points

- `python -m wikipdf` — CLI via `src/wikipdf/__main__.py`
- `wikipdf.fetcher.fetch_article(topic)` — Fetch article
- `wikipdf.pdfgen.article_to_pdf(article)` — Generate PDF