"""
=============================================================================
PHASE 4: RULE-BASED LABELING
=============================================================================
Project  : Quality Level Classification of AI-Generated Code
           Using Static Structural Metrics
File     : labeling.py

Description
-----------
Reads /data/processed/features.csv (Phase 3 output) and assigns a quality
label y ∈ {Good, Moderate, Bad} to every code sample using a deterministic
multi-feature scoring function.

Mathematical formulation
------------------------
Step 1 – Min-Max normalisation (per feature, across the full dataset):

    f̂_i = (f_i − min(f_i)) / (max(f_i) − min(f_i))   ∈ [0, 1]

Step 2 – Weighted quality score:

    Q(x̂) = Σ_i  w_i · f̂_i

    Positive w_i → higher value = WORSE quality   (complexity, depth …)
    Negative w_i → higher value = BETTER quality  (functions, comments …)

Step 3 – Decision rule:

    y = Good      if Q(x̂) <  α   (α = 0.35)
    y = Moderate  if α ≤ Q(x̂) < β (β = 0.60)
    y = Bad       if Q(x̂) ≥  β

I/O contract
------------
Input  : /data/processed/features.csv
Output : /data/processed/labeled_dataset.csv
         (all original columns + quality_score + label)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FEATURES_CSV = Path("data/processed/features.csv")
OUTPUT_CSV   = Path("data/processed/labeled_dataset.csv")

# Thresholds for the decision rule  y = f(Q)
THRESHOLD_GOOD_TO_MOD  = 0.35   # α  — below this → Good
THRESHOLD_MOD_TO_BAD   = 0.60   # β  — above this → Bad

# ---------------------------------------------------------------------------
# Feature weights   (must list the same features as extracted in Phase 3,
# excluding file_id and parse_error which are not numeric metrics)
#
#   +w  → higher raw value  = worse code  (penalise)
#   -w  → higher raw value  = better code (reward)
# ---------------------------------------------------------------------------

FEATURE_WEIGHTS: dict[str, float] = {
    # Structural / complexity  → PENALISE (positive weight)
    "loc":               0.15,
    "sloc":              0.10,
    "cyclomatic_avg":    0.25,   # heaviest penalty – most correlated with bugs
    "cyclomatic_max":    0.15,
    "nesting_depth_max": 0.15,
    "nesting_depth_avg": 0.05,
    "halstead_vocab":    0.05,

    # Modularity / readability → REWARD (negative weight)
    "function_count":    -0.10,
    "class_count":       -0.05,
    "comment_ratio":     -0.10,
    "avg_var_name_len":  -0.08,
    "unique_var_count":  -0.02,
}

# Weights must sum approximately to 0 (balanced scorer)
_wsum = sum(FEATURE_WEIGHTS.values())   # positive ≈ residual "bad" bias


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _validate_columns(df: pd.DataFrame) -> None:
    """Ensure all expected feature columns are present."""
    missing = [c for c in FEATURE_WEIGHTS if c not in df.columns]
    if missing:
        raise ValueError(
            f"features.csv is missing columns: {missing}\n"
            "Re-run feature_extraction.py to regenerate features.csv."
        )


def _drop_error_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separate rows that had parse errors from clean rows.
    Error rows still receive a label ('Unclassified') but are not
    used for normalisation statistics.
    """
    mask_ok  = ~df["parse_error"].astype(bool)
    return df[mask_ok].copy(), df[~mask_ok].copy()


# ---------------------------------------------------------------------------
# Core scoring and labelling
# ---------------------------------------------------------------------------

def compute_quality_scores(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    1. Min-Max normalise all feature columns.
    2. Compute weighted quality score Q(x̂).
    3. Assign label via decision rule.

    Returns df_clean with two new columns: quality_score, label.
    """
    feature_cols = list(FEATURE_WEIGHTS.keys())
    weights      = np.array([FEATURE_WEIGHTS[c] for c in feature_cols])

    # -- 1. Normalise --------------------------------------------------------
    scaler     = MinMaxScaler(feature_range=(0, 1))
    X_norm     = scaler.fit_transform(df_clean[feature_cols].values.astype(float))

    # -- 2. Quality score  Q = Σ w_i · f̂_i ----------------------------------
    # Raw dot product; then shift into [0,1] via min-max on scores themselves
    raw_scores = X_norm @ weights                  # shape: (n,)

    score_min  = raw_scores.min()
    score_max  = raw_scores.max()
    denom      = score_max - score_min if score_max != score_min else 1.0
    Q          = (raw_scores - score_min) / denom  # ∈ [0,1]

    df_clean = df_clean.copy()
    df_clean["quality_score"] = np.round(Q, 4)

    # -- 3. Decision rule  y = f(Q) -----------------------------------------
    def _assign_label(q: float) -> str:
        if q < THRESHOLD_GOOD_TO_MOD:
            return "Good"
        elif q < THRESHOLD_MOD_TO_BAD:
            return "Moderate"
        else:
            return "Bad"

    df_clean["label"] = df_clean["quality_score"].map(_assign_label)
    return df_clean


def label_dataset(
    features_csv: Path = FEATURES_CSV,
    output_csv:   Path = OUTPUT_CSV,
) -> pd.DataFrame:
    """
    Full Phase 4 pipeline.

    Returns the final labeled DataFrame (clean rows only; error rows
    are saved with label='Unclassified').
    """
    # -- Load ----------------------------------------------------------------
    if not features_csv.exists():
        raise FileNotFoundError(
            f"features.csv not found at {features_csv.resolve()}\n"
            "Run feature_extraction.py first."
        )
    df = pd.read_csv(features_csv)
    print(f"[Phase 4] Loaded {len(df)} rows from {features_csv}")

    _validate_columns(df)

    # -- Split clean / errored -----------------------------------------------
    df_clean, df_errors = _drop_error_rows(df)
    print(f"  Clean rows    : {len(df_clean)}")
    print(f"  Errored rows  : {len(df_errors)} (will be labelled 'Unclassified')")

    if len(df_clean) < 10:
        raise RuntimeError(
            "Too few clean rows to build a reliable label distribution. "
            "Check your data pipeline."
        )

    # -- Score and label clean rows ------------------------------------------
    df_labeled = compute_quality_scores(df_clean)

    # -- Mark errored rows ---------------------------------------------------
    if not df_errors.empty:
        df_errors = df_errors.copy()
        df_errors["quality_score"] = np.nan
        df_errors["label"]         = "Unclassified"
        df_labeled = pd.concat([df_labeled, df_errors], ignore_index=True)

    # -- Save ----------------------------------------------------------------
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_labeled.to_csv(output_csv, index=False)

    # -- Report --------------------------------------------------------------
    dist = df_labeled["label"].value_counts()
    print(f"\n[Phase 4] Labelling complete.")
    print(f"  Output : {output_csv.resolve()}")
    print(f"  Shape  : {df_labeled.shape}")
    print("\n  Label distribution:")
    for lbl, cnt in dist.items():
        pct = 100 * cnt / len(df_labeled)
        print(f"    {lbl:<14} {cnt:>4}  ({pct:.1f}%)")

    print(f"\n  Q-score summary (clean rows):")
    qs = df_labeled.loc[df_labeled["label"] != "Unclassified", "quality_score"]
    print(f"    min={qs.min():.3f}  max={qs.max():.3f}  "
          f"mean={qs.mean():.3f}  std={qs.std():.3f}")
    print(f"\n  Decision thresholds used:")
    print(f"    Good     : Q < {THRESHOLD_GOOD_TO_MOD}")
    print(f"    Moderate : {THRESHOLD_GOOD_TO_MOD} ≤ Q < {THRESHOLD_MOD_TO_BAD}")
    print(f"    Bad      : Q ≥ {THRESHOLD_MOD_TO_BAD}")

    return df_labeled


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df_out = label_dataset()
    print("\nSample (first 8 rows, selected columns):")
    cols = ["file_id", "cyclomatic_avg", "comment_ratio",
            "function_count", "quality_score", "label"]
    print(df_out[cols].head(8).to_string(index=False))
