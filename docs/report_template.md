# Final Research Report: Emergency Graph Routing

## Abstract
Brief summary of the experimental problem, algorithms investigated (static vs. dynamic routing), simulation setup, key quantitative findings, and conclusions.

## 1. Introduction & Problem Statement
- Emergency vehicle dispatching challenges under dynamic urban traffic and unexpected disruptions.
- Motivation for dynamic replanning over static precomputed routes.
- Scope of synthetic graph models and disruption scenarios.

## 2. Network Topology & Disruption Modeling
- Synthetic road network generation details (grid/planar structures, hierarchy, speed limits).
- Disruption generation: stochastic delay spikes, sudden link blockages, temporal congestion profiles.

## 3. Methodology & Routing Algorithms
- **Static Baseline**: A priori shortest path calculation (Dijkstra / A*).
- **Dynamic Routing**: Adaptive online rerouting based on updated localized/global edge state knowledge.
- Formulations, complexity analysis, and implementation details.

## 4. Experimental Setup & Metrics
- Parameters and configuration (node count, edge densities, seed set).
- Primary metrics:
  - Mean & median response time
  - Variance and tail latency (95th percentile arrival times)
  - Failure/rerouting rate
  - Computational runtime per vehicle trip

## 5. Results & Discussion
- Side-by-side path comparisons.
- Statistical significance tests and cost distribution analysis.
- Sensitivity analysis across disruption probabilities and intensities.

## 6. Conclusion & Future Work
- Summary of practical takeaways for municipal emergency dispatch systems.
- Extensions: multi-agent fleet routing, real-time sensor integration, reinforcement learning policies.
