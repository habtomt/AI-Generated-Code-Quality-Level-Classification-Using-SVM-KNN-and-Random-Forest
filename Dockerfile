# =============================================================================
# Dockerfile
# Project: Quality Level Classification of AI-Generated Code
# =============================================================================
#
# Build:   docker build -t code-quality-classifier .
# Run  :   docker run -p 8000:8000 \
#              -v $(pwd)/data:/app/data \
#              -v $(pwd)/models:/app/models \
#              -v $(pwd)/results:/app/results \
#              code-quality-classifier
#
# Then open: http://localhost:8000
# API docs : http://localhost:8000/docs
#
# Notes
# -----
# The container ships the application code only.
# Mount your data/, models/, and results/ directories from the host so that:
#   • feature_extraction.py reads  data/raw/*.py
#   • train_model.py       writes  models/*.pkl
#   • evaluate.py          writes  results/*.png / *.csv
#
# To run the full pipeline INSIDE the container in one shot:
#
#   docker run --rm \
#     -v $(pwd)/data:/app/data \
#     -v $(pwd)/models:/app/models \
#     -v $(pwd)/results:/app/results \
#     code-quality-classifier \
#     python run_pipeline.py
# =============================================================================

FROM python:3.11-slim

# ── System deps ───────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Python dependencies (cached layer) ────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ── Application code ──────────────────────────────────────────────────────────
COPY feature_extraction.py  .
COPY labeling.py             .
COPY train_model.py          .
COPY evaluate.py             .
COPY api.py                  .
COPY run_pipeline.py         .
COPY ui/                     ./ui/

# ── Create persistent directories (overridden by volume mounts) ───────────────
RUN mkdir -p data/raw data/processed models results

# ── Environment ───────────────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1
ENV MODELS_DIR=/app/models
ENV UI_DIR=/app/ui

# ── Expose port ───────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Default: start FastAPI ────────────────────────────────────────────────────
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
