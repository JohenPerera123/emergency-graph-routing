"""Verify that every expected output of the pipeline exists with the correct shape and reasonable content."""
import sys
from pathlib import Path
from typing import List
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
FIGURES_DIR = PROJECT_ROOT / "figures"

EXPECTED_CSVS = {
    "static_results.csv": [
        "trial",
        "source",
        "target",
        "static_cost",
        "static_path_length",
    ],
    "comparison_results.csv": [
        "trial",
        "source",
        "target",
        "static_cost",
        "dynamic_cost",
        "static_path_length",
        "dynamic_path_length",
        "path_differs",
    ],
    "sensitivity_results.csv": [
        "disruption_factor",
        "n_trials",
        "n_diff",
        "pct_diff",
    ],
}

EXPECTED_FIGURES = [
    "01_network_topology.png",
    "02_static_routing.png",
    "03_dynamic_routing.png",
    "04_cost_distribution.png",
    "05_sensitivity_analysis.png",
    "06_side_by_side_comparison.png",
]

MIN_FIGURE_BYTES = 10_000

checks = []


def check(description: str, condition: bool) -> None:
    """
    Record and print a single verification check.

    Args:
        description: Human-readable description of the check.
        condition: True if the check passed, False otherwise.

    Returns:
        None. Appends (description, condition) to the module-level checks list.
    """
    checks.append((description, condition))
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")


def check_csv(name: str, expected_columns: List[str]) -> None:
    """
    Verify a processed CSV exists, has the right columns, and is non-empty.

    Args:
        name: Filename (e.g., "static_results.csv").
        expected_columns: Exact column names, in order.

    Returns:
        None. Records multiple checks via the check() function.
    """
    path = DATA_DIR / name
    check(f"{name} exists", path.exists())
    if not path.exists():
        return
    try:
        df = pd.read_csv(path)
        check(f"{name} columns match", list(df.columns) == expected_columns)
        check(f"{name} has rows (>0)", len(df) > 0)
    except Exception as exc:
        check(f"{name} is readable ({exc})", False)


def check_figure(name: str) -> None:
    """
    Verify a figure exists and is non-trivial in size.

    Args:
        name: Filename (e.g., "01_network_topology.png").

    Returns:
        None. Records checks via the check() function.
    """
    path = FIGURES_DIR / name
    check(f"{name} exists", path.exists())
    if path.exists():
        size = path.stat().st_size
        check(
            f"{name} size > {MIN_FIGURE_BYTES} bytes (actual: {size})",
            size > MIN_FIGURE_BYTES,
        )


def main() -> None:
    """Run all verification checks and exit with 0 on success, 1 on any failure."""
    print("=" * 72)
    print("Verifying pipeline outputs")
    print("=" * 72 + "\n")

    print("--- Processed CSVs ---")
    for name, cols in EXPECTED_CSVS.items():
        check_csv(name, cols)
    print()

    print("--- Figures ---")
    for name in EXPECTED_FIGURES:
        check_figure(name)
    print()

    print("--- Raw networks ---")
    pkls = sorted(RAW_DIR.glob("network_*.pkl"))
    check(f"50 network pickles exist (found {len(pkls)})", len(pkls) == 50)
    print()

    n_pass = sum(1 for _, ok in checks if ok)
    n_total = len(checks)
    print("=" * 72)
    print(f"RESULT: {n_pass}/{n_total} checks passed")
    print("=" * 72)

    if n_pass == n_total:
        print("\nAll outputs verified.")
        sys.exit(0)
    else:
        print(f"\n{n_total - n_pass} check(s) failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

__all__ = ["check", "check_csv", "check_figure", "main"]
