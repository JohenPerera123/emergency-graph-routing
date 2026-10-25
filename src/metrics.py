"""Comparison metrics and sensitivity analysis for the dynamic vs static routing study."""
import random
from typing import List, Dict, Any
import pandas as pd
import networkx as nx
from src.routing import static_routing, dynamic_routing
from src.config import OVERLOAD_THRESHOLD, SEED


def summarise_comparison(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute summary statistics for the static vs dynamic comparison.

    Args:
        df: DataFrame with columns ['trial', 'source', 'target',
            'static_cost', 'dynamic_cost', 'static_path_length',
            'dynamic_path_length', 'path_differs'].

    Returns:
        A dict with keys:
            'n_trials': int
            'mean_static_cost': float
            'mean_dynamic_cost': float
            'mean_cost_delta': float (dynamic - static)
            'std_static_cost': float
            'std_dynamic_cost': float
            'n_paths_differed': int
            'pct_paths_differed': float (0-100)
    """
    n_trials = len(df)
    mean_static_cost = float(df["static_cost"].mean())
    mean_dynamic_cost = float(df["dynamic_cost"].mean())
    mean_cost_delta = mean_dynamic_cost - mean_static_cost
    std_static_cost = float(df["static_cost"].std())
    std_dynamic_cost = float(df["dynamic_cost"].std())
    n_paths_differed = int(df["path_differs"].sum())
    pct_paths_differed = 100.0 * n_paths_differed / n_trials if n_trials > 0 else 0.0

    return {
        "n_trials": n_trials,
        "mean_static_cost": mean_static_cost,
        "mean_dynamic_cost": mean_dynamic_cost,
        "mean_cost_delta": mean_cost_delta,
        "std_static_cost": std_static_cost,
        "std_dynamic_cost": std_dynamic_cost,
        "n_paths_differed": n_paths_differed,
        "pct_paths_differed": pct_paths_differed,
    }


def sensitivity_analysis(
    networks: List[nx.Graph],
    disruption_factors: List[float],
    threshold: float = OVERLOAD_THRESHOLD,
) -> pd.DataFrame:
    """
    For each disruption factor, re-run dynamic routing on all networks
    and record how often the path differs from the static baseline.

    Args:
        networks: A list of networks with capacity/load attributes.
        disruption_factors: Values of alpha to test.
        threshold: Overload threshold passed to dynamic_routing.

    Returns:
        DataFrame with columns
        ['disruption_factor', 'n_trials', 'n_diff', 'pct_diff'].
    """
    rows = []
    for factor in disruption_factors:
        n_diff = 0
        for i, G in enumerate(networks):
            rng = random.Random(SEED + i)
            nodes = list(G.nodes())
            source, target = rng.sample(nodes, 2)
            s_path, _ = static_routing(G, source=source, target=target)
            d_path, _ = dynamic_routing(
                G,
                source=source,
                target=target,
                threshold=threshold,
                disruption_factor=factor,
            )
            if s_path != d_path:
                n_diff += 1
        n_trials = len(networks)
        pct_diff = 100.0 * n_diff / n_trials if n_trials > 0 else 0.0
        rows.append({
            "disruption_factor": factor,
            "n_trials": n_trials,
            "n_diff": n_diff,
            "pct_diff": pct_diff,
        })

    return pd.DataFrame(rows)


__all__ = ["summarise_comparison", "sensitivity_analysis"]
