"""Synthetic emergency healthcare network generator."""
import random
from typing import List
import networkx as nx
import numpy as np
from src.config import (
    SEED,
    NUM_NODES,
    CONNECTION_PROB,
    NUM_TRIALS,
    EDGE_WEIGHT_MIN,
    EDGE_WEIGHT_MAX,
    CAPACITY_MIN,
    CAPACITY_MAX,
)


def generate_synthetic_network(
    seed: int = SEED,
    num_nodes: int = NUM_NODES,
    connection_prob: float = CONNECTION_PROB,
) -> nx.Graph:
    """
    Generate a synthetic emergency healthcare network.

    Nodes represent healthcare facilities (hospitals, clinics, supply depots).
    Edges represent roads or referral pathways, weighted by travel time in minutes.

    Each node carries the following attributes:
        - name (str): "Facility_<i>"
        - capacity (int): random integer in [CAPACITY_MIN, CAPACITY_MAX]
        - current_load (int): initialised to 0
        - type (str): one of "Hospital", "Clinic", "Supply_Depot"

    Each edge carries:
        - weight (int): travel time in minutes, in [EDGE_WEIGHT_MIN, EDGE_WEIGHT_MAX]

    If the generated graph is disconnected, edges are added between
    components (with random weights in [10, 25]) until the graph is
    fully connected.

    Args:
        seed: Random seed for reproducibility.
        num_nodes: Number of nodes in the network.
        connection_prob: Probability that any given pair of nodes is connected.

    Returns:
        A connected undirected weighted NetworkX graph.
    """
    random.seed(seed)
    np.random.seed(seed)

    G: nx.Graph = nx.Graph()
    facility_types: List[str] = ["Hospital", "Clinic", "Supply_Depot"]

    for i in range(num_nodes):
        G.add_node(
            i,
            name=f"Facility_{i}",
            capacity=random.randint(CAPACITY_MIN, CAPACITY_MAX),
            current_load=0,
            type=random.choice(facility_types),
        )

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < connection_prob:
                weight = random.randint(EDGE_WEIGHT_MIN, EDGE_WEIGHT_MAX)
                G.add_edge(i, j, weight=weight)

    if num_nodes > 1 and not nx.is_connected(G):
        components = [list(c) for c in nx.connected_components(G)]
        for idx in range(len(components) - 1):
            u = random.choice(components[idx])
            v = random.choice(components[idx + 1])
            edge_weight = random.randint(10, 25)
            G.add_edge(u, v, weight=edge_weight)

    return G


def generate_trials(n_trials: int = NUM_TRIALS) -> List[nx.Graph]:
    """
    Generate a list of n_trials independent synthetic networks.

    Each trial uses a different seed (SEED + trial_index) so that the
    networks are independent but fully reproducible.

    Args:
        n_trials: Number of network instances to generate.

    Returns:
        A list of n_trials NetworkX graphs.
    """
    return [generate_synthetic_network(seed=SEED + i) for i in range(n_trials)]
