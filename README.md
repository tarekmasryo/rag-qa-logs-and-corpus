# 🧠 RAG QA Logs & Corpus — Decision-Grade RAG Ops Notebook

A **production-style RAG Ops notebook + validation toolkit** that turns **multi-table RAG telemetry** into **decision-ready signals**.

This is not generic EDA — it answers operator questions:
- **Attribution:** retrieval failure vs generation failure
- **Risk slices:** where quality breaks (domain × scenario × difficulty)
- **Trade-offs:** best config under **quality × cost × latency**
- **Gating:** choose a confidence threshold for rollout (**coverage vs error**)

**Outputs:** KPI baselines, risk slice tables, config leaderboard, failure taxonomy, and threshold curves.

---

## Contents
- Notebook: `rag-qa-logs-and-corpus.ipynb`
- Dataset (Kaggle): `tarekmasryo/RAG QA Logs & Corpus Data`
- Schema notes: `docs/schema.md`

---

## 🗺️ System map (tables → signals → decisions)

```text
┌───────────────┐      ┌───────────────┐      ┌─────────────────────────┐
│   Documents   │ ───▶ │     Chunks     │ ───▶ │ Retrieval (top-k lists) │
└───────────────┘      └───────────────┘      └─────────────────────────┘
        ▲                       │                         │
        │                       ▼                         ▼
 Corpus metadata         Retrieval events            QA eval runs (labels)
        │                                                 │
        ▼                                                 ▼
 Scenarios & use cases ───────────────────────────▶ Ops KPIs + risk + gates
```

**Mapping used in the notebook**
- `documents` / `chunks` → coverage + indexing surface
- `retrieval_events` → ranks/scores (optional, deeper attribution)
- `eval_runs` → quality labels + cost/latency + recall signals
- `scenarios` → slicing keys (e.g., `scenario_type`, `difficulty`, `domain`)

---

## 📦 Expected tables

| Type | Files |
|---|---|
| Required | `rag_corpus_documents.csv`, `rag_corpus_chunks.csv`, `rag_qa_eval_runs.csv`, `rag_qa_scenarios.csv` |
| Optional | `rag_retrieval_events.csv` (drill-down), `docs/data_dictionary.csv` (column descriptions) |

---

## Quickstart

### Kaggle (recommended)
1. Open `rag-qa-logs-and-corpus.ipynb` on Kaggle  
2. Add the dataset as an input  
3. Run all cells

### Local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -U pip
pip install -e ".[notebook]"
jupyter lab
```

Put CSVs under `./data/`, or set:
```bash
export RAGQA_DATA_DIR=/path/to/csvs   # Mac/Linux
# PowerShell:
# $env:RAGQA_DATA_DIR="C:\path\to\csvs"
```

---

## Validate the dataset

Run integrity checks without Jupyter:
```bash
pip install -e .
ragqa-validate --data-dir ./data
```

---

## ✅ What the notebook does

1) **Load & verify**
- fast integrity checks: PK uniqueness + join consistency (prevents silent row blow-ups)

2) **KPI baseline**
- correctness / hallucination / faithfulness (label-aware)
- cost & latency summaries (avg + p95 when available)

3) **Coverage vs demand**
- compares corpus distribution vs eval demand (spots “high-demand / low-coverage” gaps)

4) **Risk slices**
- prioritizes **high-volume + low-quality** segments (domain × scenario × difficulty)

5) **Config trade-offs**
- compares configs across **quality × cost × latency** and highlights practical winners

6) **Failure taxonomy**
- splits failures into **retrieval vs generation** (e.g., using `recall_at_10` threshold)

7) **Confidence gate**
- simple baseline (LogisticRegression) + threshold sweep for **coverage vs error** rollout control

---

## Data & privacy note

This repo is designed for **telemetry-style logs**. If you publish derived logs:
- remove **PII** (emails, usernames, raw user prompts, internal URLs)
- anonymize / hash queries where needed
- attach a clear **data license** (the Kaggle dataset page should be the source of truth)

---

## Author
**Tarek Masryo**
