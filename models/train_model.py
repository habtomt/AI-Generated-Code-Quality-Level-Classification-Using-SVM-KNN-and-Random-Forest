"""
=============================================================================
PHASE 5: MODEL TRAINING
=============================================================================
Project  : Quality Level Classification of AI-Generated Code
           Using Static Structural Metrics
File     : train_model.py

Description
-----------
Trains three classifiers — SVM, k-Nearest Neighbour, Random Forest — on
the labeled dataset from Phase 4 with:
  • 70 / 15 / 15  stratified train / val / test split
  • 5-fold stratified cross-validation on the training fold
  • RandomizedSearchCV hyperparameter tuning per model
  • Saved .pkl artefacts and training logs

Mathematical formulation
------------------------
Dataset  D = {(x_i, y_i)}, x_i ∈ R^d, y_i ∈ {Good, Moderate, Bad}

Split:
  D_train  (70 %)  – used for CV + final fit
  D_val    (15 %)  – used for early-stopping / threshold selection
  D_test   (15 %)  – held out until evaluate.py

Objective learned by each model:
  ŷ = f(x ; θ*)   where  θ* = argmax_θ CV_accuracy(D_train, θ)

5-fold CV mean / std:
  μ_acc = (1/5) Σ acc_k
  σ_acc = sqrt( (1/5) Σ (acc_k - μ_acc)² )

I/O contract
------------
Input  : /data/processed/labeled_dataset.csv    (Phase 4 output)
Output : /models/svm.pkl
         /models/knn.pkl
         /models/random_forest.pkl
         /models/label_encoder.pkl
         /models/scaler.pkl
         /models/split_indices.pkl              (for evaluate.py)
         /models/training_log.json
"""

from __future__ import annotations

import json
import pickle
import sys
import time
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedShuffleSplit,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LABELED_CSV   = Path("data/processed/labeled_dataset.csv")
MODELS_DIR    = Path("models")

FEATURE_COLS = [
    "loc", "sloc", "cyclomatic_avg", "cyclomatic_max",
    "function_count", "class_count",
    "nesting_depth_max", "nesting_depth_avg",
    "comment_ratio", "avg_var_name_len",
    "unique_var_count", "halstead_vocab",
]
LABEL_COL    = "label"
RANDOM_STATE = 42

TRAIN_RATIO  = 0.70
VAL_RATIO    = 0.15
TEST_RATIO   = 0.15   # 1 - TRAIN - VAL

N_CV_FOLDS   = 5
N_ITER_SEARCH = 30       # RandomizedSearchCV iterations per model


# ---------------------------------------------------------------------------
# Hyperparameter search spaces
# ---------------------------------------------------------------------------

SVM_PARAM_DIST = {
    "clf__C":      [0.01, 0.1, 1, 5, 10, 50, 100],
    "clf__kernel": ["rbf", "linear", "poly"],
    "clf__gamma":  ["scale", "auto", 0.001, 0.01, 0.1],
    "clf__degree": [2, 3, 4],     # only active for poly
}

KNN_PARAM_DIST = {
    "clf__n_neighbors": list(range(3, 21)),
    "clf__weights":     ["uniform", "distance"],
    "clf__metric":      ["euclidean", "manhattan", "minkowski"],
    "clf__p":           [1, 2, 3],
}

RF_PARAM_DIST = {
    "clf__n_estimators":      [50, 100, 200, 300, 500],
    "clf__max_depth":         [None, 5, 10, 20, 30],
    "clf__min_samples_split": [2, 5, 10],
    "clf__min_samples_leaf":  [1, 2, 4],
    "clf__max_features":      ["sqrt", "log2", None],
    "clf__criterion":         ["gini", "entropy"],
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _save_pickle(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        pickle.dump(obj, fh)
    print(f"  Saved → {path}")


def _load_dataset() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load labeled_dataset.csv, drop unusable rows, encode labels.
    Returns X (n, d), y_encoded (n,), label_encoder.
    """
    df = pd.read_csv(LABELED_CSV)
    # Keep only classifiable rows
    df = df[df["label"].isin(["Good", "Moderate", "Bad"])].reset_index(drop=True)

    missing = [c for c in FEATURE_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    X  = df[FEATURE_COLS].values.astype(float)
    # Replace inf / nan with column medians
    col_medians = np.nanmedian(X, axis=0)
    for j in range(X.shape[1]):
        mask = ~np.isfinite(X[:, j])
        X[mask, j] = col_medians[j]

    le = LabelEncoder()
    y  = le.fit_transform(df[LABEL_COL].values)

    print(f"[Phase 5] Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"  Classes  : {le.classes_}")
    dist = dict(zip(*np.unique(y, return_counts=True)))
    for enc, cnt in dist.items():
        print(f"    {le.classes_[enc]:<12} {cnt:>4} samples")

    _save_pickle(le, MODELS_DIR / "label_encoder.pkl")
    return X, y, le


def _split_dataset(
    X: np.ndarray, y: np.ndarray
) -> tuple[
    np.ndarray, np.ndarray,
    np.ndarray, np.ndarray,
    np.ndarray, np.ndarray,
    dict,
]:
    """
    Stratified 70 / 15 / 15 split.
    Returns X_train, y_train, X_val, y_val, X_test, y_test, idx_dict.
    """
    n = len(y)
    # First cut: hold out 30 % for val+test
    sss1 = StratifiedShuffleSplit(
        n_splits=1, test_size=(1 - TRAIN_RATIO), random_state=RANDOM_STATE
    )
    train_idx, rest_idx = next(sss1.split(X, y))

    X_train, y_train = X[train_idx], y[train_idx]
    X_rest,  y_rest  = X[rest_idx],  y[rest_idx]

    # Second cut: split rest equally into val / test
    val_ratio_of_rest = VAL_RATIO / (VAL_RATIO + TEST_RATIO)  # = 0.5
    sss2 = StratifiedShuffleSplit(
        n_splits=1, test_size=(1 - val_ratio_of_rest), random_state=RANDOM_STATE
    )
    val_idx_local, test_idx_local = next(sss2.split(X_rest, y_rest))

    val_idx  = rest_idx[val_idx_local]
    test_idx = rest_idx[test_idx_local]

    X_val,  y_val  = X[val_idx],  y[val_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    print(f"\n[Phase 5] Split:")
    print(f"  Train : {len(train_idx)} ({100*len(train_idx)/n:.1f}%)")
    print(f"  Val   : {len(val_idx)}   ({100*len(val_idx)/n:.1f}%)")
    print(f"  Test  : {len(test_idx)}  ({100*len(test_idx)/n:.1f}%)")

    idx_dict = {
        "train": train_idx.tolist(),
        "val":   val_idx.tolist(),
        "test":  test_idx.tolist(),
    }
    _save_pickle(idx_dict, MODELS_DIR / "split_indices.pkl")
    return X_train, y_train, X_val, y_val, X_test, y_test


# ---------------------------------------------------------------------------
# Pipeline builder
# ---------------------------------------------------------------------------

def _build_pipeline(clf) -> Pipeline:
    """Wrap StandardScaler + classifier into a single sklearn Pipeline."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf",    clf),
    ])


# ---------------------------------------------------------------------------
# Training function
# ---------------------------------------------------------------------------

def _train_model(
    name:        str,
    base_clf,
    param_dist:  dict,
    X_train:     np.ndarray,
    y_train:     np.ndarray,
    X_val:       np.ndarray,
    y_val:       np.ndarray,
    save_path:   Path,
) -> dict:
    """
    1. Build pipeline.
    2. Run RandomizedSearchCV (5-fold CV on training set).
    3. Refit best estimator on full training set.
    4. Evaluate on validation set.
    5. Save .pkl.
    6. Return training log entry.
    """
    print(f"\n{'='*60}")
    print(f"  Training: {name}")
    print(f"{'='*60}")

    pipeline  = _build_pipeline(base_clf)
    cv_inner  = StratifiedKFold(n_splits=N_CV_FOLDS, shuffle=True,
                                random_state=RANDOM_STATE)

    t0 = time.perf_counter()

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_dist,
        n_iter=N_ITER_SEARCH,
        cv=cv_inner,
        scoring="accuracy",
        refit=True,
        n_jobs=-1,
        random_state=RANDOM_STATE,
        verbose=0,
        return_train_score=True,
    )
    search.fit(X_train, y_train)
    elapsed = time.perf_counter() - t0

    best_estimator = search.best_estimator_

    # -- 5-fold CV scores on training set with best params ------------------
    cv_scores = cross_val_score(
        best_estimator, X_train, y_train,
        cv=cv_inner, scoring="accuracy", n_jobs=-1
    )
    cv_mean = float(np.mean(cv_scores))
    cv_std  = float(np.std(cv_scores))

    # -- Validation accuracy -------------------------------------------------
    val_acc = float(best_estimator.score(X_val, y_val))

    # -- Save scaler from best pipeline (for API re-use) --------------------
    if name == "Random Forest":   # save once (all share same scaler logic)
        _save_pickle(best_estimator.named_steps["scaler"],
                     MODELS_DIR / "scaler.pkl")

    _save_pickle(best_estimator, save_path)

    print(f"  Best params     : {search.best_params_}")
    print(f"  CV accuracy     : {cv_mean:.4f} ± {cv_std:.4f}  ({N_CV_FOLDS}-fold)")
    print(f"  Val accuracy    : {val_acc:.4f}")
    print(f"  Training time   : {elapsed:.1f}s")

    log_entry = {
        "model":            name,
        "best_params":      search.best_params_,
        "cv_mean_accuracy": round(cv_mean, 4),
        "cv_std_accuracy":  round(cv_std,  4),
        "cv_scores":        [round(s, 4) for s in cv_scores.tolist()],
        "val_accuracy":     round(val_acc, 4),
        "train_time_s":     round(elapsed, 2),
        "n_train":          len(y_train),
        "n_val":            len(y_val),
    }
    return log_entry


# ---------------------------------------------------------------------------
# Main training pipeline
# ---------------------------------------------------------------------------

def run_training(
    labeled_csv: Path = LABELED_CSV,
    models_dir:  Path = MODELS_DIR,
) -> dict:
    """
    Orchestrates Phases 5 model training.
    Returns the training log dictionary.
    """
    models_dir.mkdir(parents=True, exist_ok=True)

    X, y, le = _load_dataset()
    X_train, y_train, X_val, y_val, X_test, y_test = _split_dataset(X, y)

    training_log = {
        "feature_cols":  FEATURE_COLS,
        "label_classes": le.classes_.tolist(),
        "split":         {"train": TRAIN_RATIO, "val": VAL_RATIO, "test": TEST_RATIO},
        "cv_folds":      N_CV_FOLDS,
        "models":        [],
    }

    models_config = [
        (
            "SVM",
            SVC(probability=True, random_state=RANDOM_STATE, cache_size=512),
            SVM_PARAM_DIST,
            models_dir / "svm.pkl",
        ),
        (
            "kNN",
            KNeighborsClassifier(),
            KNN_PARAM_DIST,
            models_dir / "knn.pkl",
        ),
        (
            "Random Forest",
            RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
            RF_PARAM_DIST,
            models_dir / "random_forest.pkl",
        ),
    ]

    for name, clf, params, path in models_config:
        entry = _train_model(
            name, clf, params,
            X_train, y_train, X_val, y_val,
            path,
        )
        training_log["models"].append(entry)

    # -- Save log ------------------------------------------------------------
    log_path = models_dir / "training_log.json"
    with open(log_path, "w") as fh:
        json.dump(training_log, fh, indent=2)
    print(f"\n[Phase 5] Training log saved → {log_path}")

    # -- Summary table -------------------------------------------------------
    print(f"\n{'='*60}")
    print(f"  TRAINING SUMMARY")
    print(f"{'='*60}")
    print(f"  {'Model':<16} {'CV Acc':>8} {'± Std':>8} {'Val Acc':>8}")
    print(f"  {'-'*44}")
    for m in training_log["models"]:
        print(f"  {m['model']:<16} "
              f"{m['cv_mean_accuracy']:>8.4f} "
              f"{m['cv_std_accuracy']:>8.4f} "
              f"{m['val_accuracy']:>8.4f}")
    print(f"{'='*60}\n")

    print("[Phase 5] All models trained and saved.")
    print(f"  Test set ({len(y_test)} samples) is reserved for evaluate.py")

    return training_log


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_training()
