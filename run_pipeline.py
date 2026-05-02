"""
=============================================================================
run_pipeline.py  –  Full Pipeline Runner
=============================================================================
Executes Phase 3 → 4 → 5 → 6 in sequence.
Run this after placing your .py files in data/raw/.

Usage:
  python run_pipeline.py                     # full pipeline
  python run_pipeline.py --from-phase 5      # resume from Phase 5
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def banner(msg: str) -> None:
    line = "=" * 64
    print(f"\n{line}")
    print(f"  {msg}")
    print(f"{line}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full quality classification pipeline")
    parser.add_argument("--from-phase", type=int, default=3,
                        choices=[3, 4, 5, 6],
                        help="Start from this phase (default: 3)")
    args = parser.parse_args()

    start_phase = args.from_phase
    t_total     = time.perf_counter()

    # ── Phase 3: Feature Extraction ──────────────────────────────────────
    if start_phase <= 3:
        banner("PHASE 3: Feature Extraction")
        from features.feature_extraction import run_extraction
        t0 = time.perf_counter()
        run_extraction()
        print(f"\n  ✓ Phase 3 done in {time.perf_counter() - t0:.1f}s")

    # ── Phase 4: Labeling ────────────────────────────────────────────────
    if start_phase <= 4:
        banner("PHASE 4: Rule-Based Labeling")
        from labeling.labeling import label_dataset
        t0 = time.perf_counter()
        label_dataset()
        print(f"\n  ✓ Phase 4 done in {time.perf_counter() - t0:.1f}s")

    # ── Phase 5: Model Training ──────────────────────────────────────────
    if start_phase <= 5:
        banner("PHASE 5: Model Training")
        from models.train_model import run_training
        t0 = time.perf_counter()
        run_training()
        print(f"\n  ✓ Phase 5 done in {time.perf_counter() - t0:.1f}s")

    # ── Phase 6: Evaluation ──────────────────────────────────────────────
    if start_phase <= 6:
        banner("PHASE 6: Evaluation")
        from models.evaluate import run_evaluation
        t0 = time.perf_counter()
        run_evaluation()
        print(f"\n  ✓ Phase 6 done in {time.perf_counter() - t0:.1f}s")

    elapsed = time.perf_counter() - t_total
    banner(f"Pipeline complete in {elapsed:.1f}s  →  Start API: uvicorn api:app --port 8000")


if __name__ == "__main__":
    main()
