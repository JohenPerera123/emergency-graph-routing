"""Visualisation functions for the emergency healthcare network project. All plotting functions save their output to the figures/ directory and use a consistent visual style."""
from pathlib import Path
from typing import Union, List, Optional
import matplotlib.pyplot as plt
import networkx as nx


def plot_network(
    G: nx.Graph,
    title: str,
    filename: Union[str, Path],
    node_color: str = "lightblue",
    node_size: int = 500,
    figsize: tuple = (12, 8),
    seed: int = 42,
) -> None:
    """
    Visualise a NetworkX graph and save it to a file.

    Nodes are drawn with labels and a spring layout (deterministic
    via the seed parameter). Edge weights are not shown on the plot.

    Args:
        G: The graph to visualise.
        title: Title displayed above the plot.
        filename: Path where the figure will be saved (PNG).
        node_color: Colour of the nodes.
        node_size: Size of the nodes in the plot.
        figsize: Figure size as (width, height) in inches.
        seed: Random seed for the spring layout (deterministic output).

    Returns:
        None. Side effect: writes a PNG file to disk and displays the figure.
    """
    fig, ax = plt.subplots(figsize=figsize)
    pos = nx.spring_layout(G, seed=seed)
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_color,
        node_size=node_size,
        font_size=9,
        edge_color="gray",
        width=1.5,
        alpha=0.9,
    )
    ax.set_title(title, fontsize=13)
    plt.tight_layout()
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"[Figure saved] {filename}")


def plot_network_with_path(
    G: nx.Graph,
    path: Optional[List[int]],
    title: str,
    filename: Union[str, Path],
    node_color: str = "lightblue",
    path_color: str = "red",
    node_size: int = 500,
    figsize: tuple = (12, 8),
    seed: int = 42,
) -> None:
    """
    Visualise a NetworkX graph and highlight a given path.

    All nodes are drawn; edges on the path are highlighted in path_color.
    Nodes on the path are drawn with path_color.

    Args:
        G: The graph to visualise.
        path: Ordered list of node ids on the route to highlight.
              If None or empty, all nodes use node_color.
        title: Title displayed above the plot.
        filename: Path where the figure will be saved (PNG).
        node_color: Colour of nodes NOT on the path.
        path_color: Colour of nodes and edges on the path.
        node_size: Size of the nodes in the plot.
        figsize: Figure size as (width, height) in inches.
        seed: Random seed for the spring layout.

    Returns:
        None. Side effect: writes a PNG file to disk and displays the figure.
    """
    fig, ax = plt.subplots(figsize=figsize)
    pos = nx.spring_layout(G, seed=seed)
    if path:
        path_set = set(path)
        node_colors = [path_color if n in path_set else node_color for n in G.nodes()]
    else:
        node_colors = node_color
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        node_size=node_size,
        font_size=9,
        edge_color="gray",
        width=1.5,
        alpha=0.9,
    )
    if path and len(path) >= 2:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=path_edges,
            edge_color=path_color,
            width=3.5,
        )
    ax.set_title(title, fontsize=13)
    plt.tight_layout()
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"[Figure saved] {filename}")


__all__ = ["plot_network", "plot_network_with_path"]
