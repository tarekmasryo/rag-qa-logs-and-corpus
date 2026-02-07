# 🧠 RAG QA Logs & Corpus — Decision-Grade RAG Ops Notebook

A **production-style RAG Ops notebook** that turns **multi-table RAG telemetry** into **decision-ready signals**.

This is not generic EDA — it answers operator questions:

- **Attribution:** retrieval failure vs generation failure  
- **Risk slices:** where quality breaks (domain × scenario × difficulty)  
- **Trade-offs:** best config under **quality × cost × latency**  
- **Gating:** pick a threshold to control **coverage vs error** for rollout

**Outputs:** KPI baselines, risk slice tables, config leaderboard, failure taxonomy, and threshold curves.

---

## Notebook
- `rag-qa-logs-and-corpus.ipynb`

## Dataset (Kaggle)
- `tarekmasryo/RAG QA Logs & Corpus Data`

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
- `scenarios` → traffic mix for slicing (`scenario_type`, `difficulty`, `domain`)

---

## 📦 Tables expected

**Required**
- `rag_corpus_documents.csv`
- `rag_corpus_chunks.csv`
- `rag_qa_eval_runs.csv`
- `rag_qa_scenarios.csv`

**Optional**
- `rag_retrieval_events.csv` → enables query → retrieved chunks drill-down

**Docs**
- `docs/data_dictionary.csv` (schema helper; loaded if present)

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

## ⚙️ Run

### Kaggle (recommended)
1. Open the notebook on Kaggle.
2. Add the dataset (above) as an input.
3. Run all cells.

### Local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
jupyter lab
```

Place CSVs under:
- `./data/` (same filenames)
- optional: `./docs/data_dictionary.csv`

---

## Author

**Tarek Masryo**
