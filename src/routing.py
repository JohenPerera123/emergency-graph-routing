"""Routing algorithms for the emergency healthcare network. Provides the static Dijkstra baseline. The dynamic capacity-aware variant is added in Phase 4."""
from typing import Optional, List, Tuple
import networkx as nx
from src.config import OVERLOAD_THRESHOLD


def static_routing(
    G: nx.Graph,
    source: int,
    target: int,
    weight: str = "weight",
) -> Tuple[Optional[List[int]], float]:
    """
    Compute the shortest path from source to target using static edge weights.

    This is the baseline method: Dijkstra's algorithm on the graph's
    original edge weights, with no awareness of node capacity or load.

    Args:
        G: The weighted NetworkX graph.
        source: Source node id.
        target: Target node id.
        weight: Edge attribute to use as the cost (default "weight").

    Returns:
        A tuple (path, cost) where path is the list of node ids along
        the shortest path and cost is the total weight of that path.
        If no path exists, returns (None, float('inf')).
    """
    try:
        path = nx.shortest_path(G, source=source, target=target, weight=weight)
        cost = nx.shortest_path_length(G, source=source, target=target, weight=weight)
        return (path, float(cost))
    except nx.NetworkXNoPath:
        return (None, float("inf"))


def dynamic_routing(
    G: nx.Graph,
    source: int,
    target: int,
    weight: str = "weight",
    threshold: float = OVERLOAD_THRESHOLD,
    disruption_factor: float = 2.0,
) -> Tuple[Optional[List[int]], float]:
    """
    Compute the shortest path using capacity-aware dynamic edge weights.

    Proposed method: edges incident to any node whose
    current_load / capacity ratio exceeds `threshold` are penalised
    by multiplying their weight by `disruption_factor`. Dijkstra is
    then run on the penalised graph. This simulates a dispatcher
    routing traffic around overloaded facilities.

    Args:
        G: The weighted NetworkX graph. Every node must have
           "capacity" and "current_load" attributes.
        source: Source node id.
        target: Target node id.
        weight: Edge attribute to use as the base cost.
        threshold: Load/capacity ratio above which a node is
                   considered overloaded.
        disruption_factor: Multiplier applied to edges touching an
                           overloaded node.

    Returns:
        A tuple (path, cost) where path is the list of node ids along
        the dynamic shortest path and cost is the total dynamic weight
        of that path. If no path exists, returns (None, float('inf')).
    """
    G_dyn = G.copy()
    for u, v, data in G_dyn.edges(data=True):
        for node in (u, v):
            cap = G_dyn.nodes[node]["capacity"]
            load = G_dyn.nodes[node]["current_load"]
            if cap > 0 and load / cap > threshold:
                data[weight] = data[weight] * disruption_factor
                break

    try:
        path = nx.shortest_path(G_dyn, source=source, target=target, weight=weight)
        cost = nx.shortest_path_length(G_dyn, source=source, target=target, weight=weight)
        return (path, float(cost))
    except nx.NetworkXNoPath:
        return (None, float("inf"))


__all__ = ["static_routing", "dynamic_routing"]
