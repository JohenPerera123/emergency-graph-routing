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


def plot_side_by_side(
    G: nx.Graph,
    static_path: Optional[List[int]],
    dynamic_path: Optional[List[int]],
    static_cost: float,
    dynamic_cost: float,
    title: str,
    filename: Union[str, Path],
    figsize: tuple = (16, 7),
    seed: int = 42,
) -> None:
    """
    Create a side-by-side comparison of static and dynamic routing.

    Left panel: static route (red). Right panel: dynamic route (blue).
    Both panels use the same spring layout so the routes are visually comparable.

    Args:
        G: The graph.
        static_path: Node list of the static route.
        dynamic_path: Node list of the dynamic route.
        static_cost: Total cost of the static route.
        dynamic_cost: Total cost of the dynamic route.
        title: Overall figure title (suptitle).
        filename: Output path.
        figsize: Figure size.
        seed: Spring layout seed.

    Returns:
        None. Side effect: writes a PNG file to disk.
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    pos = nx.spring_layout(G, seed=seed)

    nx.draw(
        G,
        pos,
        ax=axes[0],
        with_labels=True,
        node_color="lightblue",
        node_size=500,
        font_size=9,
        edge_color="gray",
        width=1.5,
        alpha=0.9,
    )
    if static_path and len(static_path) >= 2:
        static_edges = list(zip(static_path[:-1], static_path[1:]))
        nx.draw_networkx_edges(
            G,
            pos,
            ax=axes[0],
            edgelist=static_edges,
            edge_color="red",
            width=3.5,
        )
    axes[0].set_title(f"Static Routing\nCost: {static_cost:.1f}")

    nx.draw(
        G,
        pos,
        ax=axes[1],
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_size=9,
        edge_color="gray",
        width=1.5,
        alpha=0.9,
    )
    if dynamic_path and len(dynamic_path) >= 2:
        dynamic_edges = list(zip(dynamic_path[:-1], dynamic_path[1:]))
        nx.draw_networkx_edges(
            G,
            pos,
            ax=axes[1],
            edgelist=dynamic_edges,
            edge_color="blue",
            width=3.5,
        )
    axes[1].set_title(f"Dynamic Routing\nCost: {dynamic_cost:.1f}")

    fig.suptitle(title, fontsize=15)
    plt.tight_layout()
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"[Figure saved] {filename}")


__all__ = ["plot_network", "plot_network_with_path", "plot_side_by_side"]
