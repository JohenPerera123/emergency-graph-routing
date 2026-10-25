# Dynamic vs Static Graph Models for Emergency Healthcare Networks

This research project evaluates and compares static shortest-path routing against dynamic real-time rerouting models on synthetic emergency healthcare networks under operational disruptions. Using weighted, capacity-constrained graphs representing regional healthcare infrastructure (hospitals, clinics, and supply depots), the study measures how online adaptation mitigates travel delays, bottlenecks, and unexpected network congestion.

**Project Status: Phase 1 complete (scaffolding)**

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

Generate a reproducible synthetic healthcare network:

```python
from src.graph_generator import generate_synthetic_network

G = generate_synthetic_network(seed=42)
print(G.number_of_nodes(), G.number_of_edges())
```

## Roadmap

- [x] **Phase 1**: Project Scaffolding
- [ ] **Phase 2**: Synthetic Network Generation & Baseline
- [ ] **Phase 3**: Static Routing Evaluation
- [ ] **Phase 4**: Dynamic Routing Comparison & Sensitivity Analysis
- [ ] **Phase 5**: Master Pipeline & Publication Figures
- [ ] **Phase 6**: Interactive Dashboard & UI

## Reproducibility Pipeline

To regenerate every result in this repository from scratch, run:

```bash
python pipeline/run_all.py
```

To independently verify all generated outputs without running the notebooks:

```bash
python pipeline/verify_outputs.py
```

**Note (macOS):** Use `.venv/bin/python` or activate the venv first (`source .venv/bin/activate`). macOS does not ship a bare `python` command.