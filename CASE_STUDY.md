# Case Study — RAG QA Logs & Corpus

## Overview

This repository provides a compact workflow for analyzing synthetic RAG QA logs across retrieval behavior, answer quality, hallucination risk, latency, cost, and threshold trade-offs.

It combines:

- a Kaggle-ready notebook,
- a small schema-aware validation CLI,
- sample tests for the dataset contract,
- and a concise repo structure suitable for public portfolio review.

## Problem

RAG systems can fail in several different ways:

- the retriever misses the expected evidence,
- the answer generator fails even when useful evidence is retrieved,
- hallucination risk concentrates in specific slices,
- a configuration improves quality but increases latency or cost,
- aggregate metrics hide weak domains or difficult scenario types.

The goal of this project is to make those failure modes easier to inspect from offline evaluation logs.

## Goals

### Functional goals

- Validate that required CSV tables exist and can join correctly.
- Check primary keys and foreign-key relationships.
- Build clear views for quality, retrieval behavior, cost, and latency.
- Identify higher-risk slices by domain, scenario type, and difficulty.
- Compare retrieval/model configurations using transparent offline scoring.
- Simulate threshold trade-offs on already-labeled evaluation logs.

### Engineering goals

- Keep the workflow reproducible and lightweight.
- Use simple Python tooling suitable for Kaggle and local execution.
- Separate dataset validation from notebook analysis.
- Avoid presenting the diagnostic baseline as a deployable policy model.

## Dataset contract

The companion dataset is organized as a small relational corpus:

- `rag_corpus_documents.csv` — document-level metadata.
- `rag_corpus_chunks.csv` — chunk-level rows linked to documents.
- `eval_runs.csv` — QA evaluation runs and answer-quality signals.
- `rag_retrieval_events.csv` — retrieved chunks per example/run when available.
- `scenarios.csv` — scenario metadata such as domain, type, and difficulty.
- `data_dictionary.csv` — optional human-readable schema helper.

The validator checks:

- required file presence,
- required columns,
- primary-key uniqueness,
- document-to-chunk joins,
- eval-run-to-scenario joins,
- optional retrieval-event joins when retrieval logs are present.

See [`docs/schema.md`](docs/schema.md) for the concise schema reference.

## Approach

### 1) Validate structure first

Before drawing conclusions, the repo checks whether the tables are structurally usable: missing files, duplicated IDs, and broken joins are surfaced early.

### 2) Analyze useful slices

The notebook avoids relying only on aggregate scores. It breaks results down by domain, scenario type, difficulty, retrieval setup, and generator model.

### 3) Separate retrieval and answer failure

When retrieval events are available, the analysis estimates whether weaker outcomes are more likely retrieval-side or generation-side.

### 4) Compare configurations with trade-offs

The configuration view combines quality, hallucination rate, cost, and latency into a transparent offline score. The score is a shortlist aid, not a universal objective.

### 5) Simulate thresholds offline

The threshold section shows how a probability threshold changes coverage and observed error on a held-out split. This is an offline diagnostic, not a live gating policy.

## Deliverables

- `rag_qa_logs_corpus.ipynb` — main analysis notebook.
- `ragqa-validate` — CLI for dataset integrity validation.
- `docs/schema.md` — file and join contract.
- `tests/data` — tiny sample dataset for CI validation.
- `artifacts/` — placeholder for generated outputs.

## Limitations

- The dataset is synthetic and offline.
- Real RAG applications may use different telemetry schemas.
- The baseline model is diagnostic and should not be treated as a production gate.
- Threshold choices should be validated against explicit quality, latency, and cost requirements before any live use.

## Recommended next steps

- Add more time-based slices if timestamped logs are available.
- Track configuration changes across evaluation batches.
- Add regression tests for critical metrics if this evolves into a larger evaluation workflow.
- Export key notebook tables to `artifacts/` for easier review in pull requests or releases.
