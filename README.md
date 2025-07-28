# PDF Outline Extractor

Extract structured outlines (title + hierarchical headings) from PDF documents, with full multilingual support, packaged for both local development and production via Docker.

## Overview

In many research or enterprise contexts, PDF documents are the lingua franca—but they lack native structure for machines to parse and reason over. **PDF Outline Extractor** solves this by:

* **Automatically detecting the document title**, even across languages and fonts
* **Extracting headings** (H1, H2, H3) along with their page numbers
* **Emitting a clean, semantic JSON** format for downstream consumption
* **Operating at scale**: processes up to 50-page PDFs in under 10 seconds on commodity hardware

This tool forms the core of the “Connecting the Dots” hackathon challenge: enabling intelligent, interactive document reading experiences.

## Key Features

* **Multilingual support**: English, Japanese, Chinese, Arabic, and more
* **Title detection**: robust heuristics based on font metrics and position
* **Heading hierarchy**: detects and classifies H1-H3 levels
* **Lightweight**: no external network calls, <10s per 50-page document on an 8‑CPU, 16 GB RAM machine
* **Production-grade**: Docker-ready, non-root containers, healthchecks, and volume mounts

## Architecture & Design

1. **PDF Parsing Layer**: powered by PyMuPDF for fast, reliable low‑level PDF access
2. **Language Support Module**: normalizes text encoding and directionality for RTL scripts
3. **Heuristics Engine**: analyzes font sizes, styles, and spatial positioning to infer structure
4. **JSON Serializer**: emits `{ title: string, outline: [ { level, text, page } ] }`

## Quickstart: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/nybzmr/ConnectingTheDots1A.git
cd ConnectingTheDots1A

# 2. Create & activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate         # Linux / macOS
# venv\Scripts\activate.bat    # Windows PowerShell

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run against a sample PDF
mkdir -p input output
cp path/to/sample.pdf input/
python main.py --input-dir input --output-dir output

# 5. Inspect the generated JSON
jq . output/sample.json
```

## Docker Deployment

Build a production image (AMD64):

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

Run the container (bind‑mounting local folders):

```bash
docker run --rm \
  -v "$(pwd)/input:/home/appuser/app/input" \
  -v "$(pwd)/output:/home/appuser/app/output" \
  --network none \
  pdf-outline-extractor:latest
```

## Configuration

* `--input-dir`: path to folder containing `.pdf` files (default: `./input`)
* `--output-dir`: path to write `.json` files (default: `./output`)
* `--log-level`: one of `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Logging & Monitoring

Logs are emitted to STDOUT in structured JSON lines for easy aggregation:

```json
{ "timestamp": "2025-07-29T12:00:00Z", "level": "INFO", "message": "Processed 50 pages in 2.3s" }
```

Healthchecks (in Docker): the container responds to Docker’s `HEALTHCHECK` and exits if the `main.py` process stops.

## Testing

Run unit tests (pytest required):

```bash
pytest tests/
```

## CI/CD

* GitHub Actions workflows included for linting, type‑checking, and end‑to‑end smoke tests against sample PDFs.

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit with clear, atomic messages
4. Submit a pull request targeting `main`

## License

MIT License © 2025 Nayaab Zameer Qazi
