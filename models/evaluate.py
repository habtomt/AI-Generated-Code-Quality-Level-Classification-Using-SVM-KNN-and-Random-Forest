"""
=============================================================================
PHASE 6: MODEL EVALUATION
=============================================================================
Project  : Quality Level Classification of AI-Generated Code
           Using Static Structural Metrics
File     : evaluate.py

Description
-----------
Loads the three trained models and evaluates them on the held-out test set
produced in Phase 5. Computes per-model and aggregated 5-fold CV statistics.

Metrics computed
----------------
  Per model:
    • Accuracy
    • Macro / Weighted Precision, Recall, F1
    • Confusion matrix (saved as PNG)
    • ROC-AUC (One-vs-Rest, macro-averaged)  → ROC curves saved as PNG

  Cross-validation:
    • Accuracy mean ± std (from training_log.json – already computed)

  Comparison table saved to /results/evaluation_report.csv

I/O contract
------------
Input  : /data/processed/labeled_dataset.csv
         /models/*.pkl
         /models/split_indices.pkl
         /models/label_encoder.pkl
         /models/training_log.json
Output : /results/confusion_matrix_<model>.png
         /results/roc_curve_<model>.png
         /results/evaluation_report.csv
         /results/evaluation_summary.txt
"""

from __future__ import annotations

import json
import pickle
import textwrap
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")          # non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    auc,
)
from sklearn.preprocessing import LabelBinarizer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LABELED_CSV   = Path("data/processed/labeled_dataset.csv")
MODELS_DIR    = Path("models")
RESULTS_DIR   = Path("results")

FEATURE_COLS = [
    "loc", "sloc", "cyclomatic_avg", "cyclomatic_max",
    "function_count", "class_count",
    "nesting_depth_max", "nesting_depth_avg",
    "comment_ratio", "avg_var_name_len",
    "unique_var_count", "halstead_vocab",
]

MODEL_FILES = {
    "SVM":           MODELS_DIR / "svm.pkl",
    "kNN":           MODELS_DIR / "knn.pkl",
    "Random Forest": MODELS_DIR / "random_forest.pkl",
}

PLOT_DPI = 150


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _load_pickle(path: Path) -> Any:
    with open(path, "rb") as fh:
        return pickle.load(fh)


def _ensure_results_dir() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Confusion matrix plot
# ---------------------------------------------------------------------------

def _plot_confusion_matrix(
    y_true:      np.ndarray,
    y_pred:      np.ndarray,
    class_names: list[str],
    model_name:  str,
) -> Path:
    cm   = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=True, cmap="Blues")
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=13, pad=12)
    plt.tight_layout()

    save_path = RESULTS_DIR / f"confusion_matrix_{model_name.replace(' ', '_').lower()}.png"
    fig.savefig(save_path, dpi=PLOT_DPI)
    plt.close(fig)
    print(f"  Saved → {save_path}")
    return save_path


# ---------------------------------------------------------------------------
# ROC curve plot  (One-vs-Rest, per class)
# ---------------------------------------------------------------------------

def _plot_roc_curves(
    y_true:      np.ndarray,
    y_prob:      np.ndarray,
    class_names: list[str],
    model_name:  str,
) -> tuple[Path, float]:
    """
    Compute and plot OvR ROC curves for every class.
    Returns (save_path, macro_roc_auc).
    """
    lb      = LabelBinarizer()
    y_bin   = lb.fit_transform(y_true)         # (n, n_classes) or (n, 1)
    n_cls   = len(class_names)

    # LabelBinarizer on 2 classes returns (n,1); fix to (n,2)
    if y_bin.shape[1] == 1 and n_cls == 2:
        y_bin = np.hstack([1 - y_bin, y_bin])

    fig, ax = plt.subplots(figsize=(7, 6))
    colors  = plt.cm.tab10(np.linspace(0, 0.5, n_cls))

    auc_scores = []
    for i, (cls, color) in enumerate(zip(class_names, colors)):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob[:, i])
        roc_auc     = auc(fpr, tpr)
        auc_scores.append(roc_auc)
        ax.plot(fpr, tpr, color=color, lw=2,
                label=f"{cls}  (AUC = {roc_auc:.3f})")

    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random")
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.05])
    ax.set_xlabel("False Positive Rate", fontsize=11)
    ax.set_ylabel("True Positive Rate",  fontsize=11)
    ax.set_title(f"ROC Curves (OvR) — {model_name}", fontsize=13)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    save_path = RESULTS_DIR / f"roc_curve_{model_name.replace(' ', '_').lower()}.png"
    fig.savefig(save_path, dpi=PLOT_DPI)
    plt.close(fig)
    print(f"  Saved → {save_path}")

    macro_auc = float(np.mean(auc_scores))
    return save_path, macro_auc


# ---------------------------------------------------------------------------
# Core evaluation function
# ---------------------------------------------------------------------------

def _evaluate_one_model(
    name:        str,
    pipeline,
    X_test:      np.ndarray,
    y_test:      np.ndarray,
    le,
    cv_log:      dict,
) -> dict:
    """
    Evaluate a single trained pipeline on the test set.
    Returns a result dictionary.
    """
    print(f"\n{'='*60}")
    print(f"  Evaluating: {name}")
    print(f"{'='*60}")

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)

    class_names = le.classes_.tolist()

    # -- Metrics -------------------------------------------------------------
    report = classification_report(
        y_test, y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    acc       = report["accuracy"]
    prec_mac  = report["macro avg"]["precision"]
    rec_mac   = report["macro avg"]["recall"]
    f1_mac    = report["macro avg"]["f1-score"]
    prec_wt   = report["weighted avg"]["precision"]
    rec_wt    = report["weighted avg"]["recall"]
    f1_wt     = report["weighted avg"]["f1-score"]

    print(classification_report(
        y_test, y_pred,
        target_names=class_names,
        zero_division=0,
    ))

    # -- Confusion matrix plot -----------------------------------------------
    _plot_confusion_matrix(y_test, y_pred, class_names, name)

    # -- ROC curve plot ------------------------------------------------------
    _, roc_auc = _plot_roc_curves(y_test, y_prob, class_names, name)
    print(f"  Macro ROC-AUC : {roc_auc:.4f}")

    # -- Pull CV stats from training log -------------------------------------
    cv_mean = cv_log.get("cv_mean_accuracy", float("nan"))
    cv_std  = cv_log.get("cv_std_accuracy",  float("nan"))
    cv_scores = cv_log.get("cv_scores",      [])

    print(f"  CV Accuracy   : {cv_mean:.4f} ± {cv_std:.4f}  "
          f"(folds: {cv_scores})")

    return {
        "model":              name,
        "test_accuracy":      round(acc,      4),
        "precision_macro":    round(prec_mac, 4),
        "recall_macro":       round(rec_mac,  4),
        "f1_macro":           round(f1_mac,   4),
        "precision_weighted": round(prec_wt,  4),
        "recall_weighted":    round(rec_wt,   4),
        "f1_weighted":        round(f1_wt,    4),
        "roc_auc_macro":      round(roc_auc,  4),
        "cv_mean_accuracy":   round(cv_mean,  4),
        "cv_std_accuracy":    round(cv_std,   4),
    }


# ---------------------------------------------------------------------------
# Main evaluation pipeline
# ---------------------------------------------------------------------------

def run_evaluation(
    labeled_csv: Path = LABELED_CSV,
    models_dir:  Path = MODELS_DIR,
    results_dir: Path = RESULTS_DIR,
) -> pd.DataFrame:
    """
    Full Phase 6 pipeline.
    Returns a DataFrame with one row per model.
    """
    global RESULTS_DIR
    RESULTS_DIR = results_dir
    _ensure_results_dir()

    # -- Load dataset --------------------------------------------------------
    df = pd.read_csv(labeled_csv)
    df = df[df["label"].isin(["Good", "Moderate", "Bad"])].reset_index(drop=True)

    X  = df[FEATURE_COLS].values.astype(float)
    col_medians = np.nanmedian(X, axis=0)
    for j in range(X.shape[1]):
        mask = ~np.isfinite(X[:, j])
        X[mask, j] = col_medians[j]

    le  = _load_pickle(models_dir / "label_encoder.pkl")
    y   = le.transform(df["label"].values)

    # -- Load test indices ---------------------------------------------------
    idx_dict = _load_pickle(models_dir / "split_indices.pkl")
    test_idx = idx_dict["test"]
    X_test   = X[test_idx]
    y_test   = y[test_idx]
    print(f"[Phase 6] Test set size: {len(y_test)} samples")
    print(f"  Classes: {le.classes_}")

    # -- Load training log ---------------------------------------------------
    log_path = models_dir / "training_log.json"
    with open(log_path) as fh:
        training_log = json.load(fh)
    cv_map = {m["model"]: m for m in training_log["models"]}

    # -- Evaluate each model -------------------------------------------------
    results = []
    for name, pkl_path in MODEL_FILES.items():
        if not pkl_path.exists():
            print(f"  [SKIP] {name}: model file not found at {pkl_path}")
            continue
        pipeline = _load_pickle(pkl_path)
        entry    = _evaluate_one_model(
            name, pipeline, X_test, y_test, le,
            cv_map.get(name, {})
        )
        results.append(entry)

    if not results:
        raise RuntimeError("No models were evaluated. Check models directory.")

    # -- Save comparison table -----------------------------------------------
    report_df   = pd.DataFrame(results)
    report_path = results_dir / "evaluation_report.csv"
    report_df.to_csv(report_path, index=False)
    print(f"\n[Phase 6] Report saved → {report_path}")

    # -- Save human-readable summary -----------------------------------------
    summary_lines = [
        "=" * 70,
        "  EVALUATION SUMMARY — Quality Classification of AI-Generated Code",
        "=" * 70,
        f"  Test set size : {len(y_test)} samples",
        f"  Classes       : {le.classes_.tolist()}",
        "",
        f"  {'Model':<16} {'Test Acc':>9} {'F1 Mac':>9} {'ROC-AUC':>9} "
        f"{'CV Acc':>9} {'± Std':>7}",
        f"  {'-' * 63}",
    ]
    best_acc = -1.0
    best_model = ""
    for row in results:
        summary_lines.append(
            f"  {row['model']:<16} "
            f"{row['test_accuracy']:>9.4f} "
            f"{row['f1_macro']:>9.4f} "
            f"{row['roc_auc_macro']:>9.4f} "
            f"{row['cv_mean_accuracy']:>9.4f} "
            f"{row['cv_std_accuracy']:>7.4f}"
        )
        if row["test_accuracy"] > best_acc:
            best_acc   = row["test_accuracy"]
            best_model = row["model"]

    summary_lines += [
        f"  {'=' * 63}",
        f"  Best model (test accuracy): {best_model}  ({best_acc:.4f})",
        "",
        "  Plots saved in /results/",
    ]
    summary_text = "\n".join(summary_lines)
    print("\n" + summary_text)

    summary_path = results_dir / "evaluation_summary.txt"
    summary_path.write_text(summary_text)
    print(f"\n[Phase 6] Summary saved → {summary_path}")

    return report_df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_evaluation()
