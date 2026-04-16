# wikipdf

A CLI tool that fetches Wikipedia articles and converts them to PDF files for offline reading. Ideal for students, researchers, and anyone who needs portable access to Wikipedia content without internet.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MPL%202.0-yellow)](https://opensource.org/licenses/MPL-2.0)

---

## Why

Wikipedia contains vast knowledge, but internet access isn't always available. This tool solves two problems:

1. **Offline access** — Convert articles to PDF for reading without internet.
2. **Portable format** — PDF works on any device, unlike web browsers.

The goal is simple: fetch any Wikipedia article and get a standalone PDF file.

---

## How

### Architecture

- **Fetcher** — Uses `wikipedia-api` to fetch article content via Wikipedia API.
- **PDF Generator** — Uses `fpdf2` to create PDF documents.
- **CLI** — Built with `click` for command-line interface.
- **Cache** — Uses `requests-cache` to cache API responses.

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

One topic per line. Blank lines and lines starting with `#` are ignored:

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

## Configuration

No configuration required. Default settings in `src/wikipdf/config.py`:

- Output directory: `output/`
- PDF page size: A4
- Font sizes: 18pt (title), 14pt (section), 11pt (body)

---

## License

This project is licensed under the Mozilla Public License 2.0.  
SPDX-License-Identifier: MPL-2.0

See the LICENSE file for full details.