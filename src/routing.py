"""Routing algorithms for the emergency healthcare network. Provides the static Dijkstra baseline. The dynamic capacity-aware variant is added in Phase 4."""
from typing import Optional, List, Tuple
import networkx as nx


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


__all__ = ["static_routing"]
