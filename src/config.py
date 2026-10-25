"""Central configuration for the emergency healthcare network project. All constants, seeds, and directory paths are defined here so that notebooks and source modules stay free of magic numbers and hardcoded paths."""
from pathlib import Path
from typing import List

# Root directory of the repository
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# Simulation and generation parameters
SEED: int = 42
NUM_NODES: int = 15
CONNECTION_PROB: float = 0.4
NUM_TRIALS: int = 50
EDGE_WEIGHT_MIN: int = 5
EDGE_WEIGHT_MAX: int = 30
CAPACITY_MIN: int = 5
CAPACITY_MAX: int = 20
OVERLOAD_THRESHOLD: float = 0.7
DISRUPTION_FACTORS: List[float] = [1.0, 1.5, 2.0, 3.0]

# Directory paths
DATA_RAW_DIR: Path = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR: Path = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR: Path = PROJECT_ROOT / "figures"


def ensure_directories() -> None:
    """
    Create all output directories if they do not already exist.

    Args:
        None.

    Returns:
        None.
    """
    for directory in (DATA_RAW_DIR, DATA_PROCESSED_DIR, FIGURES_DIR):
        directory.mkdir(parents=True, exist_ok=True)


__all__ = [
    "PROJECT_ROOT",
    "SEED",
    "NUM_NODES",
    "CONNECTION_PROB",
    "NUM_TRIALS",
    "EDGE_WEIGHT_MIN",
    "EDGE_WEIGHT_MAX",
    "CAPACITY_MIN",
    "CAPACITY_MAX",
    "OVERLOAD_THRESHOLD",
    "DISRUPTION_FACTORS",
    "DATA_RAW_DIR",
    "DATA_PROCESSED_DIR",
    "FIGURES_DIR",
    "ensure_directories",
]
