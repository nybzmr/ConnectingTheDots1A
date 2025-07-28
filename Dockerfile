# Multi-stage Dockerfile for Outline Extractor
# Stage 1: Builder – install dependencies and compile any native libs
FROM --platform=linux/amd64 python:3.9-slim AS builder

# Set working dir
WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libmupdf-dev \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


# Stage 2: Final – minimal runtime image
FROM --platform=linux/amd64 python:3.9-slim

LABEL maintainer="Nayaab Zameer <nybzmr02@gmail.com>"

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels \ 
    $(ls /wheels/*.whl | xargs -n1 basename)

# Copy application code
COPY --chown=appuser:appuser . .

# Create input and output directories (bind mounts expected at runtime)
RUN mkdir -p input output \
    && chown -R appuser:appuser input output

# Switch to non-root user
USER appuser

# Environment hardening
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Default entrypoint: process all PDFs under /home/appuser/app/input
ENTRYPOINT ["python", "main.py"]

# Metadata
VOLUME ["/home/appuser/app/input", "/home/appuser/app/output"]

# Healthcheck to ensure container is alive (optional)
HEALTHCHECK --interval=30s --timeout=3s CMD pgrep -f main.py || exit 1
