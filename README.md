# wikipdf

A CLI tool that fetches Wikipedia articles and generates PDFs for offline reading.

---

## Why

Wikipedia is a valuable knowledge resource, but internet access isn't always available. This tool converts Wikipedia articles to PDF files that can be read offline on any device.

### Problem

- No offline access to Wikipedia articles
- Browser-based reading isn't ideal for long-form content

### Solution

Fetch article content via Wikipedia API and generate standalone PDF files.

---

## How

### Installation

```bash
pip install -r requirements.txt
```

### Quick Start

```bash
# Single article
python -m wikipdf fetch "Python (programming language)"

# Batch from file
python -m wikipdf bulk topics.txt

# Custom output directory
python -m wikipdf fetch "Machine learning" -o ./output/
```

### Topics File Format

One topic per line. Blank lines and `#` comments are ignored:

```
# My reading list
Python_(programming_language)
Machine_learning
Deep_learning
```

---

## What

### Features

- Single article or batch processing
- PDF output with title, summary, content, and source link
- Error tracking with logs
- Cached API responses

### Output

- PDFs: `output/Python_(programming_language).pdf`
- Errors: `output/wikipdf_errors.log`
- Successes: `output/success.txt`

### Commands

| Command | Description |
|---------|-------------|
| `fetch` | Fetch single article |
| `bulk` | Batch from file |
| `--help` | Show all options |

---

## License

MPL 2.0 — See [LICENSE](LICENSE)
