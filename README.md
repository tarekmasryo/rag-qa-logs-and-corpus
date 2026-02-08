# 🧠 RAG QA Logs & Corpus — Decision-Grade RAG Ops Notebook

A production-style **RAG Ops notebook** plus a **schema-aware validation CLI** that turns multi-table
RAG telemetry into **decision-ready signals**.

**Full case study:** `CASE_STUDY.md`

---

## ✅ What this repo gives you
This is not generic EDA. It answers operator questions teams face before/after shipping RAG:

- **Attribution:** is the failure retrieval-side or generation-side?
- **Risk slices:** where quality breaks (domain × scenario × difficulty)
- **Trade-offs:** which configuration wins under **quality × cost × latency**
- **Gating:** choose thresholds for rollout (**coverage vs error**)

**Outputs:** KPI baselines, risk slice tables, config leaderboards, failure taxonomy, and threshold curves.

---

## ⚡ Quick start

### 1) Install
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
pip install -e .

# Optional (dev): lint + tests
pip install -e ".[dev]"
```

### 2) Put data in a folder
This project expects the dataset CSVs in a single directory. See `docs/schema.md`.

Recommended local path:
```text
data/raw/
  rag_corpus_documents.csv
  rag_corpus_chunks.csv
  rag_qa_scenarios.csv
  rag_qa_eval_runs.csv
  rag_retrieval_events.csv        (optional)
```

### 3) Validate dataset integrity (CLI)
```bash
ragqa-validate --data-dir data/raw
```

Or set an env var once:
```bash
# Windows (PowerShell)
$env:RAGQA_DATA_DIR="D:\path\to\data\raw"
ragqa-validate

# macOS/Linux
export RAGQA_DATA_DIR="/path/to/data/raw"
ragqa-validate
```

### 4) Run the notebook
Open and run:
- `rag-qa-logs-and-corpus.ipynb`

The notebook reads the same data directory and exports analysis artifacts under `./artifacts/`.

---

## 🧭 Case study
**Problem:** RAG systems fail in ways that dashboards often hide (silent regressions, cost spikes, retrieval collapse).  
**Approach:** validate telemetry tables + compute decision views (quality, retrieval, cost/latency, gating).  
**Evaluation:** slice metrics by domain/scenario/difficulty; separate retrieval vs generation failures when possible.  
**Decision policy:** pick confidence thresholds that control **coverage vs error** for rollout.  
**Deliverables:** a validator CLI + exported tables/figures to support release decisions.  
**Limitations:** telemetry schemas vary across stacks; the validator enforces a strict “minimum contract”.

Read the full write-up in `CASE_STUDY.md`.

---

## 📂 Repo layout
```text
.
├── rag-qa-logs-and-corpus.ipynb   # decision-grade RAG ops notebook
├── src/ragqa/                    # validation + IO helpers + CLI
├── scripts/                      # thin entry script(s)
├── tests/                        # pytest + small sample CSVs
├── docs/schema.md                # expected files + joins
├── data/raw/README.md            # where to put your dataset
└── artifacts/README.md           # what gets exported
```

---

## 🔎 Dataset contract (minimum required)
See `docs/schema.md`. Required files (required filenames):
- `rag_corpus_documents.csv`
- `rag_corpus_chunks.csv`
- `rag_qa_scenarios.csv`
- `rag_qa_eval_runs.csv`

Optional:
- `rag_retrieval_events.csv` (enables deeper retrieval attribution)

---

## 🧪 Quality gates
- **ruff** linting (imports + correctness)
- **pytest** unit test for dataset validation
- **CI smoke validation** on the sample dataset under `tests/data`

---

## 📜 License
MIT (code). Dataset licensing depends on your data source and must be specified where you publish the dataset.
