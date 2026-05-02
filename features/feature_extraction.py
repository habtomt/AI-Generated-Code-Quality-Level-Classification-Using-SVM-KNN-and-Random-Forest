"""
=============================================================================
PHASE 3: FEATURE EXTRACTION
=============================================================================
Project  : Quality Level Classification of AI-Generated Code
           Using Static Structural Metrics
File     : feature_extraction.py
Author   : Senior Technical Lead – Pattern Recognition Systems

Description
-----------
Transforms every .py file in /data/raw/ into a numerical feature vector
x ∈ R^d and stores the full design matrix X ∈ R^(n×d) as a CSV file at
/data/processed/features.csv.

Feature vector (d = 12)
-----------------------
 f1  loc                 – Total lines of code
 f2  sloc                – Source lines (non-blank, non-comment)
 f3  cyclomatic_avg      – Mean cyclomatic complexity across all functions
 f4  cyclomatic_max      – Max cyclomatic complexity in any single function
 f5  function_count      – Number of top-level and nested functions
 f6  class_count         – Number of class definitions
 f7  nesting_depth_max   – Maximum nesting depth of control structures
 f8  nesting_depth_avg   – Average nesting depth across all blocks
 f9  comment_ratio       – comment_lines / max(loc, 1)
f10  avg_var_name_len    – Mean identifier name length
f11  unique_var_count    – Number of distinct local variable names
f12  halstead_vocab      – Distinct operator + operand count (proxy)

Mathematical formulation
------------------------
Each sample i  →  x_i = [f1, f2, …, f12] ∈ R^12
Full dataset   →  X ∈ R^(n × 12),  n ≈ 725

I/O contract
------------
Input  : /data/raw/code_XXXX.py  (UTF-8 Python source files)
Output : /data/processed/features.csv
         Columns: file_id, f1…f12  (no labels — labeling is Phase 4)
"""

from __future__ import annotations

import ast
import os
import re
import sys
import textwrap
import traceback
from dataclasses import dataclass, field, fields, asdict
from pathlib import Path
from typing import List, Optional

import pandas as pd
from radon.complexity import cc_visit
from radon.metrics import h_visit


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_DIR       = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUTPUT_CSV    = PROCESSED_DIR / "features.csv"
ENCODING      = "utf-8"


# ---------------------------------------------------------------------------
# Data container for one file's feature vector
# ---------------------------------------------------------------------------

@dataclass
class FeatureVector:
    file_id:           str   = ""
    loc:               int   = 0   # f1
    sloc:              int   = 0   # f2
    cyclomatic_avg:    float = 0.0 # f3
    cyclomatic_max:    int   = 0   # f4
    function_count:    int   = 0   # f5
    class_count:       int   = 0   # f6
    nesting_depth_max: int   = 0   # f7
    nesting_depth_avg: float = 0.0 # f8
    comment_ratio:     float = 0.0 # f9
    avg_var_name_len:  float = 0.0 # f10
    unique_var_count:  int   = 0   # f11
    halstead_vocab:    int   = 0   # f12
    parse_error:       bool  = False


# ---------------------------------------------------------------------------
# AST visitor for structural metrics
# ---------------------------------------------------------------------------

class StructuralVisitor(ast.NodeVisitor):
    """
    Single-pass AST traversal that collects:
      - function / class counts
      - maximum and per-block nesting depth
      - variable (Name, Store) identifiers
    """

    def __init__(self) -> None:
        self.function_count:   int        = 0
        self.class_count:      int        = 0
        self.nesting_depths:   List[int]  = []
        self.variable_names:   set        = set()
        self._current_depth:   int        = 0
        self._control_nodes = (
            ast.If, ast.For, ast.While, ast.With,
            ast.Try, ast.ExceptHandler, ast.AsyncFor, ast.AsyncWith,
        )

    # -- helpers -----------------------------------------------------------

    def _enter_block(self) -> None:
        self._current_depth += 1
        self.nesting_depths.append(self._current_depth)

    def _exit_block(self) -> None:
        self._current_depth -= 1

    # -- visitors ----------------------------------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.function_count += 1
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef          # treat async same

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_count += 1
        self.generic_visit(node)

    def _visit_control(self, node: ast.AST) -> None:
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()

    def visit_If(self, node):       self._visit_control(node)
    def visit_For(self, node):      self._visit_control(node)
    def visit_While(self, node):    self._visit_control(node)
    def visit_With(self, node):     self._visit_control(node)
    def visit_Try(self, node):      self._visit_control(node)
    def visit_AsyncFor(self, node): self._visit_control(node)
    def visit_AsyncWith(self, node):self._visit_control(node)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.variable_names.add(node.id)
        self.generic_visit(node)

    # -- summary properties ------------------------------------------------

    @property
    def nesting_depth_max(self) -> int:
        return max(self.nesting_depths, default=0)

    @property
    def nesting_depth_avg(self) -> float:
        if not self.nesting_depths:
            return 0.0
        return sum(self.nesting_depths) / len(self.nesting_depths)

    @property
    def avg_var_name_len(self) -> float:
        if not self.variable_names:
            return 0.0
        return sum(len(v) for v in self.variable_names) / len(self.variable_names)


# ---------------------------------------------------------------------------
# Core extraction function
# ---------------------------------------------------------------------------

def _count_loc_and_comments(source: str) -> tuple[int, int, int]:
    """
    Returns (loc, sloc, comment_lines).

    loc           = total lines (including blank)
    sloc          = non-blank, non-comment lines
    comment_lines = lines whose stripped content starts with '#'
    """
    lines         = source.splitlines()
    loc           = len(lines)
    comment_lines = sum(1 for ln in lines if ln.strip().startswith("#"))
    blank_lines   = sum(1 for ln in lines if not ln.strip())
    sloc          = loc - blank_lines - comment_lines
    return loc, max(sloc, 0), comment_lines


def _cyclomatic_metrics(source: str) -> tuple[float, int]:
    """
    Uses radon's cc_visit to compute per-function cyclomatic complexity.
    Returns (mean_cc, max_cc).

    Formula (McCabe):  CC = E - N + 2P
    radon approximates this per function/method.
    """
    try:
        results = cc_visit(source)
    except Exception:
        return 0.0, 0
    if not results:
        return 1.0, 1   # single implicit block
    complexities = [r.complexity for r in results]
    return sum(complexities) / len(complexities), max(complexities)


def _halstead_vocab(source: str) -> int:
    """
    Halstead vocabulary η = η1 + η2
      η1 = distinct operators, η2 = distinct operands.
    radon h_visit computes this per function; we take the sum across
    all functions as a proxy for module-level vocabulary.
    """
    try:
        h = h_visit(source)
        # h_visit returns a HalsteadReport named tuple or list of them
        if hasattr(h, "vocabulary"):
            return int(h.vocabulary)
        # older radon returns a dict keyed by function name
        if isinstance(h, dict):
            total = 0
            for report in h.values():
                total += getattr(report, "vocabulary", 0)
            return total
    except Exception:
        pass
    return 0


def extract_features(filepath: Path) -> FeatureVector:
    """
    Extract the full feature vector for a single Python source file.

    Algorithm
    ---------
    1. Read and decode source (UTF-8 with fallback latin-1).
    2. Count LOC / SLOC / comment lines via text scan.
    3. Compute cyclomatic complexity via radon cc_visit.
    4. Compute Halstead vocabulary via radon h_visit.
    5. Parse AST; traverse with StructuralVisitor to collect
       function/class counts, nesting depths, variable names.
    6. Bundle all metrics into FeatureVector.
    """
    fv = FeatureVector(file_id=filepath.stem)

    # -- 1. Read source -------------------------------------------------------
    try:
        source = filepath.read_text(encoding=ENCODING)
    except UnicodeDecodeError:
        try:
            source = filepath.read_text(encoding="latin-1")
        except Exception as exc:
            print(f"  [READ ERROR] {filepath.name}: {exc}", file=sys.stderr)
            fv.parse_error = True
            return fv
    except Exception as exc:
        print(f"  [READ ERROR] {filepath.name}: {exc}", file=sys.stderr)
        fv.parse_error = True
        return fv

    # -- 2. LOC / SLOC / comments  -------------------------------------------
    fv.loc, fv.sloc, comment_lines = _count_loc_and_comments(source)
    fv.comment_ratio = comment_lines / max(fv.loc, 1)

    # -- 3. Cyclomatic complexity  -------------------------------------------
    fv.cyclomatic_avg, fv.cyclomatic_max = _cyclomatic_metrics(source)

    # -- 4. Halstead vocabulary  ---------------------------------------------
    fv.halstead_vocab = _halstead_vocab(source)

    # -- 5. AST structural metrics  ------------------------------------------
    try:
        tree    = ast.parse(source)
        visitor = StructuralVisitor()
        visitor.visit(tree)

        fv.function_count    = visitor.function_count
        fv.class_count       = visitor.class_count
        fv.nesting_depth_max = visitor.nesting_depth_max
        fv.nesting_depth_avg = round(visitor.nesting_depth_avg, 4)
        fv.unique_var_count  = len(visitor.variable_names)
        fv.avg_var_name_len  = round(visitor.avg_var_name_len, 4)

    except SyntaxError as exc:
        print(f"  [SYNTAX ERROR] {filepath.name}: {exc}", file=sys.stderr)
        fv.parse_error = True
    except RecursionError:
        print(f"  [RECURSION] {filepath.name}: AST too deep", file=sys.stderr)
        fv.parse_error = True
    except Exception as exc:
        print(f"  [AST ERROR] {filepath.name}: {exc}", file=sys.stderr)
        fv.parse_error = True

    return fv


# ---------------------------------------------------------------------------
# Batch extraction
# ---------------------------------------------------------------------------

def run_extraction(
    raw_dir:    Path = RAW_DIR,
    output_csv: Path = OUTPUT_CSV,
) -> pd.DataFrame:
    """
    Scan raw_dir for .py files, extract feature vectors, write CSV.

    Output CSV schema
    -----------------
    file_id | loc | sloc | cyclomatic_avg | cyclomatic_max |
    function_count | class_count | nesting_depth_max | nesting_depth_avg |
    comment_ratio | avg_var_name_len | unique_var_count | halstead_vocab |
    parse_error

    Returns the DataFrame (all rows, including errored ones).
    """
    py_files = sorted(raw_dir.glob("*.py"))
    if not py_files:
        raise FileNotFoundError(f"No .py files found in {raw_dir.resolve()}")

    print(f"[Phase 3] Found {len(py_files)} Python files in {raw_dir}")

    records: List[FeatureVector] = []
    errors  = 0

    for i, fp in enumerate(py_files, 1):
        fv = extract_features(fp)
        records.append(fv)
        if fv.parse_error:
            errors += 1
        if i % 50 == 0 or i == len(py_files):
            print(f"  Processed {i}/{len(py_files)} files  ({errors} errors so far)")

    df = pd.DataFrame([asdict(r) for r in records])

    # -- enforce column order and dtypes -------------------------------------
    feature_cols = [
        "file_id",
        "loc", "sloc",
        "cyclomatic_avg", "cyclomatic_max",
        "function_count", "class_count",
        "nesting_depth_max", "nesting_depth_avg",
        "comment_ratio", "avg_var_name_len",
        "unique_var_count", "halstead_vocab",
        "parse_error",
    ]
    df = df[feature_cols]

    # write output
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"\n[Phase 3] Extraction complete.")
    print(f"  Total files   : {len(py_files)}")
    print(f"  Parse errors  : {errors}")
    print(f"  Output        : {output_csv.resolve()}")
    print(f"  Shape         : {df.shape}  (rows × columns)")

    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = run_extraction()
    print("\nSample (first 5 rows):")
    print(df.head().to_string(index=False))
