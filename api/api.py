"""
=============================================================================
PHASE 7: FASTAPI BACKEND  (updated — multi-model comparison support)
=============================================================================
Project  : Quality Level Classification of AI-Generated Code
           Using Static Structural Metrics
File     : api.py

Endpoints
---------
POST /predict/all                          ← PRIMARY ENDPOINT
  Run ALL loaded models, aggregate via majority-vote + confidence tiebreak.
  Body : { "code": "..." }
  Response:
    {
      "results": [
        { "model": "SVM",           "label": "Moderate", "confidence": 0.71,
          "probabilities": {...} },
        { "model": "kNN",           "label": "Good",     "confidence": 0.65,
          "probabilities": {...} },
        { "model": "Random Forest", "label": "Good",     "confidence": 0.91,
          "probabilities": {...} }
      ],
      "final_decision": {
        "label":          "Good",
        "reason":         "Majority vote (2/3) + highest confidence (Random Forest, 0.91)",
        "vote_counts":    {"Good": 2, "Moderate": 1},
        "agreement":      "partial",
        "top_model":      "Random Forest",
        "top_confidence": 0.91
      },
      "features":    { ... },
      "parse_error": false
    }

POST /predict
  Single-model prediction (legacy / programmatic use).
  Body : { "code": "...", "model_name": "random_forest" }

GET /health
GET /models

Run with:
  uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload
"""

from __future__ import annotations

import os
import pickle
import sys
import tempfile
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Re-use feature extraction from Phase 3
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent))
from features.feature_extraction import extract_features, FeatureVector   # type: ignore

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODELS_DIR = Path(os.getenv("MODELS_DIR", "models"))
UI_DIR     = Path(os.getenv("UI_DIR",     "ui"))

AVAILABLE_MODELS = {
    "SVM":           MODELS_DIR / "svm.pkl",
    "kNN":           MODELS_DIR / "knn.pkl",
    "Random Forest": MODELS_DIR / "random_forest.pkl",
}

FEATURE_COLS = [
    "loc", "sloc", "cyclomatic_avg", "cyclomatic_max",
    "function_count", "class_count",
    "nesting_depth_max", "nesting_depth_avg",
    "comment_ratio", "avg_var_name_len",
    "unique_var_count", "halstead_vocab",
]

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

_model_cache:  Dict = {}
_label_encoder       = None


def _load_models() -> None:
    global _label_encoder
    le_path = MODELS_DIR / "label_encoder.pkl"
    if le_path.exists():
        with open(le_path, "rb") as fh:
            _label_encoder = pickle.load(fh)
    else:
        print(f"WARNING: label_encoder.pkl not found at {le_path}", file=sys.stderr)

    for name, path in AVAILABLE_MODELS.items():
        if path.exists():
            with open(path, "rb") as fh:
                _model_cache[name] = pickle.load(fh)
            print(f"  Loaded model: {name}")
        else:
            print(f"  Model not found, skipping: {name} ({path})", file=sys.stderr)

    if not _model_cache:
        print("WARNING: No models loaded. Run train_model.py first.", file=sys.stderr)


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title       = "Code Quality Classifier",
    description = "Predict quality level (Good / Moderate / Bad) of Python code.",
    version     = "1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    print("[API] Loading models …")
    _load_models()
    print(f"[API] Loaded: {list(_model_cache.keys())}")


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class PredictAllRequest(BaseModel):
    code: str = Field(..., description="Raw Python source code")

class PredictRequest(BaseModel):
    code:       str           = Field(..., description="Raw Python source code")
    model_name: Optional[str] = Field(default=None,
        description="SVM | kNN | Random Forest  (default: Random Forest)")

class SingleModelResult(BaseModel):
    model:         str
    label:         str
    confidence:    float
    probabilities: Dict[str, float]

class FinalDecision(BaseModel):
    label:          str
    reason:         str
    vote_counts:    Dict[str, int]
    agreement:      str            # "full" | "partial" | "split"
    top_model:      str
    top_confidence: float

class PredictAllResponse(BaseModel):
    results:        List[SingleModelResult]
    final_decision: FinalDecision
    features:       Dict[str, float]
    parse_error:    bool

class PredictResponse(BaseModel):
    label:         str
    confidence:    float
    probabilities: Dict[str, float]
    features:      Dict[str, float]
    model_used:    str
    parse_error:   bool


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _extract_from_code(code: str):
    """Write code to temp file → extract features → return (fv, features_dict, X)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(code)
        tmp_path = Path(tmp.name)
    try:
        fv = extract_features(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    X = np.array([[getattr(fv, c, 0.0) for c in FEATURE_COLS]], dtype=float)
    for j in range(X.shape[1]):
        if not np.isfinite(X[0, j]):
            X[0, j] = 0.0

    features_out = {
        col: round(float(getattr(fv, col, 0.0)), 4)
        for col in FEATURE_COLS
    }
    return fv, features_out, X


def _run_one_model(name: str, pipeline, X: np.ndarray) -> SingleModelResult:
    """Predict with a single pipeline, return structured result."""
    y_pred_enc = pipeline.predict(X)[0]
    y_prob     = pipeline.predict_proba(X)[0]

    if _label_encoder is not None:
        label       = str(_label_encoder.inverse_transform([y_pred_enc])[0])
        class_names = _label_encoder.classes_.tolist()
    else:
        label       = str(y_pred_enc)
        class_names = [str(i) for i in range(len(y_prob))]

    confidence    = float(np.max(y_prob))
    probabilities = {cls: round(float(p), 4) for cls, p in zip(class_names, y_prob)}

    return SingleModelResult(
        model         = name,
        label         = label,
        confidence    = round(confidence, 4),
        probabilities = probabilities,
    )


def _aggregate_decisions(results: List[SingleModelResult]) -> FinalDecision:
    """
    Majority-vote + confidence tiebreak aggregation.

    Steps
    -----
    1. Count votes per label.
    2. Majority wins. Ties broken by highest-confidence supporting model.
    3. Classify agreement level: full | partial | split.
    4. Identify top model (highest confidence overall) for the reason string.
    """
    labels      = [r.label      for r in results]
    confidences = [r.confidence for r in results]
    models      = [r.model      for r in results]
    n           = len(results)

    vote_counts = dict(Counter(labels))
    max_votes   = max(vote_counts.values())
    tied_labels = [lbl for lbl, cnt in vote_counts.items() if cnt == max_votes]

    if len(tied_labels) == 1:
        winner_label = tied_labels[0]
    else:
        best_conf: Dict[str, float] = {}
        for r in results:
            if r.label in tied_labels:
                best_conf[r.label] = max(best_conf.get(r.label, 0.0), r.confidence)
        winner_label = max(best_conf, key=best_conf.get)

    if max_votes == n:
        agreement = "full"
    elif max_votes > n / 2:
        agreement = "partial"
    else:
        agreement = "split"

    top_idx        = int(np.argmax(confidences))
    top_model      = models[top_idx]
    top_confidence = round(confidences[top_idx], 4)

    vote_str = f"{max_votes}/{n}"
    if agreement == "full":
        reason = (
            f"All {n} models agree · "
            f"highest confidence: {top_model} ({top_confidence:.2f})"
        )
    elif agreement == "partial":
        reason = (
            f"Majority vote ({vote_str}) · "
            f"highest confidence: {top_model} ({top_confidence:.2f})"
        )
    else:
        reason = (
            f"Split vote — resolved by highest confidence: "
            f"{top_model} ({top_confidence:.2f})"
        )

    return FinalDecision(
        label          = winner_label,
        reason         = reason,
        vote_counts    = vote_counts,
        agreement      = agreement,
        top_model      = top_model,
        top_confidence = top_confidence,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", summary="Health check")
def health():
    return {
        "status":        "ok",
        "models_loaded": list(_model_cache.keys()),
        "label_classes": _label_encoder.classes_.tolist() if _label_encoder else [],
    }


@app.get("/models", summary="List available models")
def list_models():
    return {
        name: {"loaded": name in _model_cache, "pkl_path": str(path)}
        for name, path in AVAILABLE_MODELS.items()
    }


@app.post(
    "/predict/all",
    response_model = PredictAllResponse,
    summary        = "Predict with ALL models + majority-vote final decision",
)
def predict_all(request: PredictAllRequest) -> PredictAllResponse:
    """
    Primary endpoint — runs SVM, kNN, and Random Forest simultaneously,
    then aggregates into a single final decision via majority vote and
    confidence-weighted tiebreaking.
    """
    if not _model_cache:
        raise HTTPException(503, detail="No models loaded. Run train_model.py first.")

    fv, features_out, X = _extract_from_code(request.code)

    results = [
        _run_one_model(name, pipeline, X)
        for name, pipeline in _model_cache.items()
    ]

    final = _aggregate_decisions(results)

    return PredictAllResponse(
        results        = results,
        final_decision = final,
        features       = features_out,
        parse_error    = fv.parse_error,
    )


@app.post(
    "/predict",
    response_model = PredictResponse,
    summary        = "Single-model prediction (programmatic / backward compat)",
)
def predict(request: PredictRequest) -> PredictResponse:
    if not _model_cache:
        raise HTTPException(503, detail="No models loaded. Run train_model.py first.")

    model_name = request.model_name or "Random Forest"
    if model_name not in _model_cache:
        raise HTTPException(400, detail=f"Model '{model_name}' not loaded. "
                                        f"Available: {list(_model_cache.keys())}")

    fv, features_out, X = _extract_from_code(request.code)
    result = _run_one_model(model_name, _model_cache[model_name], X)

    return PredictResponse(
        label         = result.label,
        confidence    = result.confidence,
        probabilities = result.probabilities,
        features      = features_out,
        model_used    = model_name,
        parse_error   = fv.parse_error,
    )


# ---------------------------------------------------------------------------
# Serve frontend
# ---------------------------------------------------------------------------

if UI_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")

    @app.get("/", include_in_schema=False)
    def root():
        return FileResponse(str(UI_DIR / "index.html"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, workers=1)
