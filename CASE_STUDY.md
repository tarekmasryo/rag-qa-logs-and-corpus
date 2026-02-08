# Case Study — RAG QA Logs & Corpus (Decision-Grade RAG Ops)

## Overview
This repository provides a workflow for **RAG quality operations**: a multi-table telemetry dataset, a schema-aware validator, and an analysis notebook that turns logs into clear **release decisions**.

It focuses on the operational questions that determine whether a system is safe to ship.

## The real problem
RAG systems can degrade quietly:
- retrieval quality drops while top-line scores look “fine”
- cost and latency drift upward without clear ownership
- hallucinations rise in specific domains/scenarios
- a new prompt/model improves one slice while breaking another

If you only track aggregate metrics, you discover regressions after users do.

## Goals (definition of done)
**Functional goals**
- Validate dataset integrity across multiple CSV tables (required columns, key uniqueness, joins).
- Produce decision views: **KPI baselines**, **risk slices**, **configuration leaderboards**, and **gating curves**.

**Engineering goals**
- Enforce a strict “minimum contract” to catch broken telemetry early.
- Keep analysis reproducible and CPU-friendly (pandas / scikit-learn-style tooling).
- Provide simple entry points: CLI validation + notebook analysis.

**What success looks like**
- You can identify the top failure slices, the best configuration under quality × cost × latency, and a safe rollout threshold.

## Data contract (minimum viable telemetry)
The dataset behaves like a small relational system (CSV files as tables):

- **Documents** (`rag_corpus_documents.csv`): what the corpus contains (`doc_id`, domain, metadata)
- **Chunks** (`rag_corpus_chunks.csv`): how documents are split (`chunk_id` → `doc_id`)
- **Scenarios** (`rag_qa_scenarios.csv`): evaluation groupings (domain/type/difficulty)
- **Eval runs** (`rag_qa_eval_runs.csv`): model outputs + quality signals (`run_id` → `scenario_id`)
- *(Optional)* **Retrieval events** (`rag_retrieval_events.csv`): which chunks were retrieved (`example_id`, `chunk_id`, score)

The validator checks:
- required file presence and required columns
- primary-key uniqueness (where applicable)
- foreign-key joins (chunks → documents, eval_runs → scenarios)
- optional retrieval integrity checks when `rag_retrieval_events.csv` is present

See `docs/schema.md` for required columns and join rules.

## Approach
### 1) Integrity first (fail fast)
Before computing metrics, validate the dataset shape:
- missing files / columns
- duplicated IDs
- broken joins (orphan chunks, unknown scenarios)

This prevents drawing conclusions from corrupted telemetry.

### 2) Decision views (not presentation-first charts)
The notebook is structured around operator decisions:
- **Attribution:** retrieval vs generation failure (when retrieval events exist)
- **Risk slices:** domain × scenario_type × difficulty breakdowns
- **Trade-offs:** quality vs cost vs latency across configurations (e.g., model, prompt, retriever settings, chunking)
- **Gating:** confidence-threshold curves (coverage vs error) for rollout

### 3) Outputs
The workflow is designed to produce outputs you can attach to a release decision:
- a validation report from the CLI
- exported tables/figures under `./artifacts/`
- a short narrative of recommended actions (fix retrieval, change configuration, adjust threshold)

Typical exported files include:
- `artifacts/validation_report.json`
- `artifacts/kpi_baselines.csv`
- `artifacts/risk_slices.csv`
- `artifacts/config_leaderboard.csv`
- `artifacts/gating_curves.csv`

## Usage
Setup and execution steps are documented in `README.md`.

Minimal flow:
- Validate tables: `ragqa-validate --data-dir data/raw`
- Run the notebook: `rag-qa-logs-and-corpus.ipynb` (exports outputs under `./artifacts/`)

## Limitations
- Telemetry schemas vary widely; this repo enforces a strict minimum contract.
- Deeper attribution improves when retrieval event logs are available.
- This is a workflow template; production deployments should add access controls, redaction, and monitoring.

## Next steps
- Define a release gate policy: minimum slice quality thresholds + maximum cost/latency budgets.
- Track stability over time (weekly baselines, regressions, drift alerts).
- Integrate with CI/CD: block merges when validation fails or key metrics regress.
