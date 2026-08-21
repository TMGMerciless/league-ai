# League AI Architecture

## Goal

Build a testable League of Legends decision-support system that can ingest structured game data, model game state, evaluate decisions, and eventually provide explainable recommendations.

## High-Level Flow

Riot/static data
→ ingestion
→ normalized data
→ game-state representation
→ deterministic baseline
→ machine-learning models
→ explanation layer
→ UI/API

## Engineering Principles

- Build one layer at a time.
- Keep data collection separate from model inference.
- Establish deterministic baselines before adding ML.
- Measure model performance against baselines.
- Keep components modular and testable.
- Track experiments, failures, and lessons learned.
