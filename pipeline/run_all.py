"""Master pipeline. Regenerates all data and figures by executing the three notebooks end-to-end, then verifies that every expected output exists with the correct shape."""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

NOTEBOOKS = [
    "01_data_generation",
    "02_static_baseline",
    "03_dynamic_comparison",
]


def run_notebook(name: str) -> None:
    """
    Execute a single notebook in-place via nbconvert.

    Args:
        name: Notebook stem (without .ipynb extension), relative to
              the notebooks/ directory.

    Returns:
        None. Raises SystemExit with the subprocess return code on failure.
    """
    nb_path = PROJECT_ROOT / "notebooks" / f"{name}.ipynb"
    if not nb_path.exists():
        print(f"[ERROR] Notebook not found: {nb_path}")
        sys.exit(1)

    print("=" * 72)
    print(f"Executing: {nb_path.name}")
    print("=" * 72)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            str(nb_path),
        ],
        check=False,
    )

    if result.returncode != 0:
        print(f"\n[FAILED] {nb_path.name} (exit code {result.returncode})")
        sys.exit(result.returncode)

    print(f"[OK]     {nb_path.name}\n")


def main() -> None:
    """Run all notebooks in order, then verify outputs."""
    print("\n" + "=" * 72)
    print("Master pipeline: regenerating all results")
    print("=" * 72 + "\n")

    for name in NOTEBOOKS:
        run_notebook(name)

    print("=" * 72)
    print("All notebooks executed successfully.")
    print("Running output verification...")
    print("=" * 72 + "\n")

    verify_script = PROJECT_ROOT / "pipeline" / "verify_outputs.py"
    result = subprocess.run([sys.executable, str(verify_script)], check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

__all__ = ["run_notebook", "main"]
