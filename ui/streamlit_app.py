"""Streamlit dashboard for the emergency healthcare network routing study. Loads precomputed results and provides interactive exploration of static vs dynamic routing."""
import sys
from pathlib import Path
import pickle
import random
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
from scipy import stats

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    SEED,
    NUM_TRIALS,
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    FIGURES_DIR,
    OVERLOAD_THRESHOLD,
    DISRUPTION_FACTORS,
)
from src.routing import static_routing, dynamic_routing
from src.metrics import summarise_comparison

# Page config (must be the first Streamlit call)
st.set_page_config(
    page_title="Emergency Healthcare Routing Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏥 Emergency Healthcare Network Routing")
st.markdown("**Static vs Dynamic Capacity-Aware Routing Comparison**")
st.markdown("---")


@st.cache_data
def load_networks():
    """Load all 50 networks from data/raw/."""
    networks = []
    for i in range(NUM_TRIALS):
        with open(DATA_RAW_DIR / f"network_{i:02d}.pkl", "rb") as f:
            networks.append(pickle.load(f))
    return networks


@st.cache_data
def load_static_results():
    """Load static baseline CSV."""
    return pd.read_csv(DATA_PROCESSED_DIR / "static_results.csv")


@st.cache_data
def load_comparison_results():
    """Load comparison CSV."""
    return pd.read_csv(DATA_PROCESSED_DIR / "comparison_results.csv")


@st.cache_data
def load_sensitivity_results():
    """Load sensitivity CSV."""
    return pd.read_csv(DATA_PROCESSED_DIR / "sensitivity_results.csv")


# Sidebar controls
st.sidebar.header("Controls")

trial_id = st.sidebar.selectbox(
    "Select Trial",
    options=list(range(NUM_TRIALS)),
    index=0,
    help="Choose which of the 50 synthetic networks to explore",
)

disruption_factor = st.sidebar.slider(
    "Disruption Factor (α)",
    min_value=1.0,
    max_value=5.0,
    value=2.0,
    step=0.1,
    help="Multiplier applied to edges touching overloaded nodes",
)

threshold = st.sidebar.slider(
    "Overload Threshold",
    min_value=0.3,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Load/capacity ratio above which a node is considered overloaded",
)

show_weights = st.sidebar.checkbox("Show edge weights on plot", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard compares a **static Dijkstra** baseline against a "
    "**capacity-aware dynamic** routing model. The dynamic model penalises "
    "edges incident to overloaded facilities, simulating real-time rerouting."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Trial Explorer",
    "📈 Aggregate Results",
    "🔬 Sensitivity Analysis",
    "📋 Data Table",
])

with tab1:
    st.subheader(f"Trial {trial_id}: Static vs Dynamic Routing")

    networks = load_networks()
    G = networks[trial_id].copy()

    # Assign loads (same protocol as Notebook 03: SEED + 1000 + trial_id)
    rng = random.Random(SEED + 1000 + trial_id)
    for node in G.nodes():
        cap = G.nodes[node]["capacity"]
        G.nodes[node]["current_load"] = rng.randint(0, cap)

    # Select source/target (same protocol as Notebook 02/03: SEED + trial_id)
    rng2 = random.Random(SEED + trial_id)
    nodes = list(G.nodes())
    default_source, default_target = rng2.sample(nodes, 2)

    col_src, col_tgt = st.columns(2)
    with col_src:
        source = st.selectbox("Source node", options=nodes, index=nodes.index(default_source))
    with col_tgt:
        target = st.selectbox("Target node", options=nodes, index=nodes.index(default_target))

    static_path, static_cost = static_routing(G, source=source, target=target)
    dynamic_path, dynamic_cost = dynamic_routing(
        G,
        source=source,
        target=target,
        threshold=threshold,
        disruption_factor=disruption_factor,
    )

    overloaded = [
        n
        for n in G.nodes()
        if G.nodes[n]["capacity"] > 0
        and G.nodes[n]["current_load"] / G.nodes[n]["capacity"] > threshold
    ]
    st.info(
        f"**{len(overloaded)} / {G.number_of_nodes()}** nodes overloaded "
        f"(load/capacity > {threshold:.2f})"
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Static Cost", f"{static_cost:.1f} min")
    col2.metric("Dynamic Cost", f"{dynamic_cost:.1f} min")
    col3.metric("Cost Delta", f"{dynamic_cost - static_cost:+.1f} min")
    col4.metric("Paths Differ", "✅ Yes" if static_path != dynamic_path else "❌ No")

    st.markdown("### Network Comparison")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    pos = nx.spring_layout(G, seed=42)

    # Left: static
    nx.draw(
        G,
        pos,
        ax=axes[0],
        with_labels=True,
        node_color="lightblue",
        node_size=500,
        font_size=8,
        edge_color="gray",
        width=1.5,
    )
    if static_path and len(static_path) >= 2:
        edges = list(zip(static_path[:-1], static_path[1:]))
        nx.draw_networkx_edges(
            G, pos, ax=axes[0], edgelist=edges, edge_color="red", width=3.5
        )
    if show_weights:
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=axes[0], font_size=7
        )
    axes[0].set_title(f"Static Route (Cost: {static_cost:.1f})")

    # Right: dynamic
    nx.draw(
        G,
        pos,
        ax=axes[1],
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_size=8,
        edge_color="gray",
        width=1.5,
    )
    if dynamic_path and len(dynamic_path) >= 2:
        edges = list(zip(dynamic_path[:-1], dynamic_path[1:]))
        nx.draw_networkx_edges(
            G, pos, ax=axes[1], edgelist=edges, edge_color="blue", width=3.5
        )
    if show_weights:
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=axes[1], font_size=7
        )
    axes[1].set_title(f"Dynamic Route (Cost: {dynamic_cost:.1f})")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Show path details"):
        st.write(f"**Static path:** {static_path}  (cost: {static_cost:.2f})")
        st.write(f"**Dynamic path:** {dynamic_path}  (cost: {dynamic_cost:.2f})")

    with st.expander("Show node load table"):
        node_rows = []
        for n in G.nodes():
            cap = G.nodes[n]["capacity"]
            load = G.nodes[n]["current_load"]
            node_rows.append({
                "Node": n,
                "Type": G.nodes[n]["type"],
                "Capacity": cap,
                "Load": load,
                "Load/Capacity": load / cap if cap > 0 else 0,
                "Overloaded": load / cap > threshold if cap > 0 else False,
            })
        st.dataframe(pd.DataFrame(node_rows), use_container_width=True)

with tab2:
    st.subheader("Aggregate Results Across 50 Trials")

    comp_df = load_comparison_results()
    summary = summarise_comparison(comp_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Static Cost", f"{summary['mean_static_cost']:.2f} min")
    col2.metric("Mean Dynamic Cost", f"{summary['mean_dynamic_cost']:.2f} min")
    col3.metric("Paths Differed", f"{summary['pct_paths_differed']:.1f}%")

    st.markdown("### Cost Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(comp_df))
    width = 0.35
    ax.bar(
        x - width / 2,
        comp_df["static_cost"],
        width,
        label="Static",
        color="steelblue",
        alpha=0.8,
    )
    ax.bar(
        x + width / 2,
        comp_df["dynamic_cost"],
        width,
        label="Dynamic",
        color="coral",
        alpha=0.8,
    )
    ax.set_xlabel("Trial")
    ax.set_ylabel("Cost (minutes)")
    ax.set_title("Static vs Dynamic Routing Cost by Trial")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    diffs = comp_df["dynamic_cost"] - comp_df["static_cost"]
    nonzero = diffs[diffs != 0]
    if len(nonzero) >= 5:
        stat, p = stats.wilcoxon(nonzero, zero_method="wilcox")
        st.markdown("### Statistical Test")
        st.markdown(
            f"**Wilcoxon signed-rank test** (n = {len(nonzero)}): "
            f"statistic = {stat:.4f}, p-value = {p:.6f}"
        )
        if p < 0.05:
            st.success("Result: significant difference (reject H0 at α = 0.05)")
        else:
            st.warning("Result: no significant difference (fail to reject H0)")

with tab3:
    st.subheader("Sensitivity Analysis: Effect of Disruption Factor")

    sens_df = load_sensitivity_results()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        sens_df["disruption_factor"],
        sens_df["pct_diff"],
        marker="o",
        linewidth=2.5,
        markersize=10,
        color="darkblue",
    )
    for _, row in sens_df.iterrows():
        ax.annotate(
            f"{row['pct_diff']:.0f}%",
            (row["disruption_factor"], row["pct_diff"]),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=10,
        )
    ax.set_xlabel("Disruption factor α", fontsize=12)
    ax.set_ylabel("% of trials where paths differ", fontsize=12)
    ax.set_title(
        "Static vs Dynamic Path Divergence vs Disruption Factor", fontsize=13
    )
    ax.grid(alpha=0.3)
    ax.set_ylim(-5, 105)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("### Sensitivity Data")
    st.dataframe(sens_df, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "**Interpretation:** The percentage of trials where the dynamic model "
        "selects a different path increases monotonically with the disruption "
        "factor. At α = 1.0 (no penalty), paths never differ. At α = 3.0, "
        "approximately one in four paths diverges — confirming that the "
        "capacity-penalty mechanism systematically alters routing decisions."
    )

with tab4:
    st.subheader("Comparison Results (All 50 Trials)")
    comp_df = load_comparison_results()

    def highlight_diff(row):
        """Highlight rows in table where static and dynamic paths differ."""
        if row["path_differs"]:
            return ["background-color: #d4edda"] * len(row)
        return [""] * len(row)

    st.dataframe(
        comp_df.style.apply(highlight_diff, axis=1),
        use_container_width=True,
        height=600,
    )

    st.markdown(
        f"**Rows where paths differed:** "
        f"{int(comp_df['path_differs'].sum())} / {len(comp_df)}"
    )

    csv = comp_df.to_csv(index=False)
    st.download_button(
        label="Download comparison_results.csv",
        data=csv,
        file_name="comparison_results.csv",
        mime="text/csv",
    )

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85em;'>"
    "Graph Theory Research Assignment — Emergency Healthcare Network Routing"
    "</div>",
    unsafe_allow_html=True,
)
