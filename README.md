# League AI

An experimental AI/ML engineering project exploring data-driven League of Legends analysis, decision support, and personalized coaching.

The project is being built from first principles as a learning-focused AI/ML engineering system rather than as a wrapper around an existing large language model.

## Project Goals

- Learn AI and machine learning from first principles.
- Build a reliable League of Legends data pipeline.
- Represent League game state in a machine-readable format.
- Develop deterministic baselines before introducing machine learning.
- Train and evaluate models against measurable objectives.
- Explore explainable and personalized League analysis.
- Maintain engineering integrity, reproducibility, and testability.

## Current Architecture

```text
Riot Data Dragon
       |
       v
Version Discovery
       |
       v
Raw Data Ingestion
       |
       v
data/raw/<patch>/
       |
       v
Champion Normalization
       |
       v
data/normalized/<patch>/
       |
       v
Feature Engineering
       |
       v
Decision / ML Models
       |
       v
Explanation & Application Layer
```

Raw and normalized datasets are generated locally and intentionally excluded from Git because they can be reproduced from the ingestion and normalization pipelines.

## Current Progress

### Environment

- Ubuntu development environment
- Python virtual environment
- NVIDIA CUDA-capable GPU
- PyTorch with GPU acceleration
- Git/GitHub development workflow

### AI/ML Foundations

Experiments completed so far include:

- CPU vs. GPU tensor computation
- Artificial neuron implementation
- Weighted inputs and bias
- ReLU activation
- Loss and gradients
- Backpropagation concepts
- Gradient descent
- Learning-rate experimentation
- Convergence and divergence

### League Data Pipeline

The current pipeline:

1. Discovers the locally available Data Dragon patch.
2. Loads versioned Riot champion data.
3. Preserves the original raw JSON.
4. Normalizes Riot's schema into a project-controlled schema.
5. Produces normalized records for all available champions.

The normalized champion representation currently includes:

- Champion identity and roles
- Riot metadata
- Base combat statistics
- Per-level stat growth
- Passive information
- Q/W/E/R ability information
- Cooldowns
- Costs
- Ranges
- Ability descriptions and semantic tooltips

## Repository Structure

```text
league-ai/
├── data/
│   ├── raw/                 # Generated Riot source data (ignored)
│   └── normalized/          # Generated normalized data (ignored)
├── docs/
│   ├── architecture.md
│   ├── champion-schema.md
│   ├── journal/
│   └── learning/
├── notebooks/
├── scripts/
├── src/
│   ├── data_ingest.py
│   └── normalize_champions.py
├── tests/
├── .gitignore
└── README.md
```

## Development Philosophy

Build one layer at a time.

Each layer should have a clear definition of done and be tested before additional complexity is introduced.

The project documents successes, failures, experiments, engineering decisions, and lessons learned throughout development.

The general engineering workflow is:

```text
Understand
   ↓
Build
   ↓
Verify
   ↓
Test
   ↓
Document
   ↓
Commit
```

## Engineering Focus

This project is being developed as an end-to-end AI/ML engineering exercise, including:

- Linux-based development
- NVIDIA CUDA and PyTorch
- Data ingestion and transformation pipelines
- Data normalization
- Feature engineering
- Neural-network fundamentals
- Model training and evaluation
- Deterministic baseline development
- API and application architecture
- Automated testing
- Reproducible development
- Git-based version control
- Technical documentation

## Next Milestone

The next development milestone is automated validation and testing of the champion normalization pipeline before additional League datasets or ML features are introduced.

## Status

Active development.

The project is intentionally iterative. Architecture and implementation decisions may change as experiments reveal better approaches.
