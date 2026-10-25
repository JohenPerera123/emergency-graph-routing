# Project Specification — Emergency Healthcare Network Graph Routing

## 1. Mission

Build a complete Graph Theory research project that compares **static vs dynamic shortest-path routing** on synthetic emergency healthcare networks. The output is:

- 3 Jupyter notebooks (data generation → static baseline → dynamic comparison)
- A reusable Python `src/` library
- 6 figures for the report
- 3 CSV result files
- A master pipeline that regenerates everything
- (Optional) a Streamlit UI

## 2. Tech Stack

- Python 3.10+
- Libraries: `networkx`, `pandas`, `numpy`, `matplotlib`, `scipy`, `jupyter`, `nbconvert`, `nbformat`
- Optional UI: `streamlit`
- Style: PEP8, type hints on all public functions, docstrings on everything

## 3. Non-Negotiable Rules

1. **No hardcoded paths.** Use `pathlib.Path` and import from `src/config.py`.
2. **Every function has a docstring** with Args / Returns.
3. **Every notebook starts with a Markdown cell** explaining its purpose.
4. **Each logical operation = one cell.** Never more than ~25 lines of code per cell.
5. **Every figure is saved** to `figures/` with the exact filename from the spec.
6. **Every notebook ends** by exporting its results to CSV.
7. **All randomness uses `SEED`** from `src/config.py` so results are reproducible.

## 4. Folder Structure

emergency-graph-routing/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/
│   ├── project_spec.md              ← the MD file for Antigravity
│   ├── report_template.md           ← your final report (from earlier)
│   └── references.md                ← paper list + links
│
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_static_baseline.ipynb
│   └── 03_dynamic_comparison.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py                    ← all constants (SEED, NUM_NODES, etc.)
│   ├── graph_generator.py           ← generate_synthetic_network()
│   ├── routing.py                   ← static_routing(), dynamic_routing()
│   ├── metrics.py                   ← comparison metrics + stats
│   └── visualize.py                 ← every plotting function
│
├── data/
│   ├── raw/                         ← generated network instances (.pkl)
│   └── processed/
│       ├── static_results.csv
│       ├── dynamic_results.csv
│       └── comparison_results.csv
│
├── figures/
│   ├── 01_network_topology.png
│   ├── 02_static_routing.png
│   ├── 03_dynamic_routing.png
│   ├── 04_cost_distribution.png
│   ├── 05_sensitivity_analysis.png
│   └── 06_side_by_side_comparison.png
│
├── pipeline/
│   └── run_all.py                   ← master pipeline (executes all 3 notebooks)
│
└── ui/                              ← Phase 5 (optional)
    ├── streamlit_app.py             ← PRIMARY UI (recommended)
    └── electron/                    ← STRETCH GOAL (only if time allows)
        ├── package.json
        ├── main.js
        ├── preload.js
        └── renderer/
            ├── index.html
            ├── styles.css
            └── renderer.js

## 5. Phase Plan

### Phase 1 — Scaffolding (30 min)

Create:
- `requirements.txt` with exactly these lines: