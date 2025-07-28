# PDF Outline Extractor

Extracts structured outlines (title + headings) from PDF documents with multilingual support.

## Features

- 📄 PDF to structured JSON conversion
- 🌍 Multilingual support (English, Japanese, Chinese, Arabic, etc.)
- 🏷️ Automatic title detection
- 🔍 Heading hierarchy detection (H1-H3)
- 🐳 Docker-ready deployment
- ⚡ Fast processing (<10s for 50-page PDFs)

## Requirements

- Python
- Docker (optional)

## Installation

### Local Setup
```bash
git clone https://github.com/nybzmr/ConnectingTheDots1A.git
cd pdf-outline-extractor
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt