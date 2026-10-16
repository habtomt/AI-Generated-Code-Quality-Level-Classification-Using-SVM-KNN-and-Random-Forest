# Quality Level Classification of LLM-Generated Python Code Using Static Structural Metrics

A machine learning pipeline that classifies AI-generated Python source files into three quality levels (**Good**, **Moderate**, **Bad**) using static structural metrics. It includes a FastAPI backend, a browser-based interface, and Docker packaging.

## Overview

LLM code generators such as GitHub Copilot and OpenAI Codex now produce large volumes of Python code whose structural quality varies widely. Manual review does not scale to that volume. This project extracts measurable properties from source files **without executing them** and uses supervised classifiers to predict a quality label.

Each file is represented as a 12-dimensional feature vector built from Abstract Syntax Tree (AST) analysis and the [Radon](https://radon.readthedocs.io/) static analysis library.

## Key Results

On a held-out test set of 107 samples:

| Model | Test Acc. | Precision (M) | Recall (M) | F1 (M) | ROC-AUC (M) | CV Acc. ± Std |
|---|---|---|---|---|---|---|
| **SVM** | **0.9720** | 0.9375 | 0.9333 | **0.9353** | **0.9990** | **0.9820 ± 0.0147** |
| kNN | 0.9065 | 0.9263 | 0.7187 | 0.7560 | 0.9492 | 0.8778 ± 0.0183 |
| Random Forest | 0.8972 | 0.8399 | 0.7560 | 0.7829 | 0.9770 | 0.8838 ± 0.0306 |

*(M = macro-averaged. ROC-AUC uses a One-vs-Rest strategy.)*

The **SVM** was the best model on every criterion. It also handled the minority **Bad** class far better than kNN and Random Forest.

### SVM Confusion Matrix (test set, n = 107)

| | Pred: Bad | Pred: Good | Pred: Moderate |
|---|---|---|---|
| **True: Bad** | 6 | 0 | 1 |
| **True: Good** | 0 | 65 | 0 |
| **True: Moderate** | 1 | 1 | 33 |

## Dataset

- About **725 AI-generated Python files**, named `code_XXXX.py`.
- Generated with prompts adapted from the *Invisible Hands* study (Zhang et al., 2025) and its public implementation.
- Tasks include algorithmic implementations, data-processing scripts, and object-oriented class structures.
- Class distribution: Good is the largest class, followed by Moderate, then Bad.
- Preprocessing:
  - Files are read as UTF-8, with a Latin-1 fallback.
  - Files with syntax errors are flagged without interrupting the pipeline.
  - Missing or non-finite feature values are imputed with column-wise medians.

## Features

Twelve static features are extracted from each file:

| ID | Feature | Description |
|---|---|---|
| f1 | LOC | Total lines of code |
| f2 | SLOC | Non-blank, non-comment executable lines |
| f3 | Cyclomatic Avg | Mean McCabe complexity across all functions |
| f4 | Cyclomatic Max | Maximum cyclomatic complexity in any function |
| f5 | Function Count | Number of function definitions |
| f6 | Class Count | Number of class definitions |
| f7 | Nesting Depth Max | Maximum control-flow nesting level |
| f8 | Nesting Depth Avg | Mean nesting depth across control blocks |
| f9 | Comment Ratio | Comment lines / total LOC |
| f10 | Avg Variable Length | Mean character length of variable identifiers |
| f11 | Unique Variable Count | Distinct local variable names |
| f12 | Halstead Vocabulary | Distinct operators + distinct operands (η = η₁ + η₂) |

## Methodology

### Rule-based labeling

Labels come from a deterministic scoring function, not from human annotation:

1. Each feature is min-max normalised to [0, 1].
2. A weighted linear score is computed: `Q(x̂) = Σ wⱼ · f̂ⱼ`. Positive weights penalise complexity, and negative weights reward modularity and documentation.
3. The score is rescaled to [0, 1] and thresholded:

| Label | Condition |
|---|---|
| Good | `Q < 0.35` |
| Moderate | `0.35 ≤ Q < 0.60` |
| Bad | `Q ≥ 0.60` |

### Models

All models are scikit-learn `Pipeline`s (`StandardScaler` → classifier), so scaling is fitted only on the training partition to prevent data leakage.

- **Support Vector Machine**, with probability estimates via Platt scaling.
- **k-Nearest Neighbours**.
- **Random Forest**.

### Experimental setup

- **Split:** stratified 70% train / 15% validation / 15% test. The test indices are serialised and kept fixed across all experiments.
- **Tuning:** `RandomizedSearchCV` with 5-fold stratified cross-validation on the training partition only, sampling 30 configurations per model and selecting by mean CV accuracy.
- **Metrics:** accuracy, macro precision, macro recall, macro F1, macro ROC-AUC (OvR), and confusion matrices.

| Model | Search space |
|---|---|
| SVM | `C` ∈ {0.01, 0.1, 1, 5, 10, 50, 100}; kernel ∈ {rbf, linear, poly}; gamma ∈ {scale, auto, 0.001, 0.01, 0.1} |
| kNN | `k` ∈ {3 … 20}; weights ∈ {uniform, distance}; metric ∈ {Euclidean, Manhattan, Minkowski} |
| Random Forest | `n_estimators` ∈ {50, 100, 200, 300, 500}; `max_depth` ∈ {None, 5, 10, 20, 30}; `max_features` ∈ {sqrt, log2, None}; `criterion` ∈ {gini, entropy} |

## System Architecture

- **Backend:** FastAPI served by Uvicorn.
- **Endpoint:** `POST /predict/all` accepts raw Python source code and returns predictions from all three models at once.
- **Ensemble decision:** majority vote with confidence-weighted tiebreaking produces a final label.
- **Frontend:** a single-page HTML/JavaScript interface where you paste or upload code and see a per-model comparison table plus the final decision.
- **Deployment:** Docker, with model artefacts, data, and results directories mounted as external volumes for persistence and reproducible retraining.

## Tech Stack

Python 3.11 · scikit-learn (≥ 1.3) · Radon (≥ 6.0) · `ast` (standard library) · Matplotlib (≥ 3.7) · FastAPI · Uvicorn · Docker

## Getting Started

> replace the commands, image name, and paths below with the ones used in this repo.

```bash
# Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### Run with Docker

```bash
docker build -t code-quality-classifier .
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  code-quality-classifier
```

Then open `http://localhost:8000` in your browser.

### Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload   # adjust module path
```

### Example API call

```bash
curl -X POST http://localhost:8000/predict/all \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b):\n    return a + b"}'
```

## Limitations

- Labels are generated by a deterministic rule-based function rather than expert human annotation, so they may not fully match practitioner judgement of code quality.
- Because the labels are a function of the same features the models see, the high scores partly measure how well the models recover the scoring rule.
- The dataset contains only Python files.
- The features are purely static. There are no semantic or dynamic metrics such as test coverage, runtime performance, or design-pattern adherence.
