# 🧠 RAG QA Logs & Corpus

**Ops, risk, and retrieval-evaluation diagnostics for synthetic RAG QA logs.**

This repository contains a Kaggle-ready notebook and a small validation utility for working with a synthetic, multi-table RAG evaluation corpus. It focuses on practical evaluation signals for retrieval behavior, answer quality, hallucination risk, cost, latency, and threshold trade-offs.

**Full case study:** [`CASE_STUDY.md`](CASE_STUDY.md)

---

## ✨ What this repo gives you

This is not a generic EDA notebook. It is structured around the kinds of questions you ask after collecting RAG QA logs:

- 🔎 **Failure attribution** — is the miss more likely coming from retrieval coverage or answer generation?
- ⚠️ **Risk slices** — which domains, scenario types, or difficulty levels show weaker quality?
- ⚖️ **Configuration trade-offs** — which retrieval/model setup balances quality, cost, and latency best?
- 🎚️ **Threshold simulation** — how does a probability threshold change shown coverage versus observed error on labeled logs?
- 🧪 **Dataset validation** — are the table keys, joins, and required files structurally valid?

**Outputs include:** KPI baselines, risk-slice tables, configuration frontiers, retrieval-vs-generation attribution, a diagnostic baseline model, and threshold trade-off views.

---

## 📦 Repository contents

```text
.
├── rag_qa_logs_corpus.ipynb      # Kaggle-ready analysis notebook
├── src/ragqa/                    # validation + IO helpers + CLI
├── scripts/                      # thin script entry points
├── tests/                        # pytest tests + tiny sample CSVs
├── docs/schema.md                # expected files, keys, and joins
├── data/raw/README.md            # local data placeholder
├── artifacts/README.md           # generated outputs placeholder
├── CASE_STUDY.md                 # concise technical write-up
└── README.md
```

---

## 🗂️ Dataset files

The notebook expects the companion dataset files in one folder:

```text
rag_corpus_documents.csv
rag_corpus_chunks.csv
eval_runs.csv
rag_retrieval_events.csv
scenarios.csv
data_dictionary.csv              # optional but recommended
```

The validation CLI requires the core tables:

```text
rag_corpus_documents.csv
rag_corpus_chunks.csv
eval_runs.csv
scenarios.csv
```

`rag_retrieval_events.csv` is optional for the CLI, but recommended because it enables deeper retrieval attribution.

---

## 🚀 Quick start

### 1) Create an environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

For development checks:

```bash
pip install -e ".[dev]"
```

### 3) Add the data locally

Place the CSV files under:

```text
data/raw/
```

Or point the CLI to another folder with `--data-dir`.

### 4) Validate the dataset

```bash
ragqa-validate --data-dir data/raw
```

You can also set an environment variable:

```bash
# Windows PowerShell
$env:RAGQA_DATA_DIR="D:\path\to\data\raw"
ragqa-validate

# macOS/Linux
export RAGQA_DATA_DIR="/path/to/data/raw"
ragqa-validate
```

### 5) Run the notebook

Open:

```text
rag_qa_logs_corpus.ipynb
```

On Kaggle, attach the companion dataset before running the notebook.

---

## 🧪 Quality checks

This repo includes a small validation path for maintainability:

- ✅ `pytest` test for the sample dataset contract
- ✅ `ruff` linting configuration
- ✅ GitHub Actions workflow for lint + tests + sample validation
- ✅ CLI smoke validation against `tests/data`

Run locally:

```bash
pytest
ruff check src tests scripts
ragqa-validate --data-dir tests/data
```

---

## 📊 Notebook focus

The notebook follows the system end-to-end:

1. **Documents and chunks** — corpus structure and coverage.
2. **Evaluation runs** — answer correctness, hallucination flags, cost, and latency.
3. **Retrieval events** — evidence recovery and retrieval/generation attribution.
4. **Scenario slices** — domain, scenario type, and difficulty risk patterns.
5. **Configuration comparison** — quality/cost/latency scoring as an offline diagnostic.
6. **Threshold simulation** — coverage versus error on already-labeled evaluation logs.

---

## ⚠️ Scope note

This project uses a synthetic/offline evaluation dataset. It is useful for analysis, benchmarking, and RAG observability practice. It is **not live customer telemetry**, and the baseline model in the notebook is **diagnostic**, not a deployable production policy.

---


## 📜 License

MIT — see [`LICENSE`](LICENSE). Dataset licensing should be specified separately wherever the dataset is published.
