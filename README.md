# 🧠 RAG QA Logs & Corpus — RAG Ops Storytelling Notebook

**Notebook:** `rag_qa_logs_and_corpus.ipynb`  
**Dataset:** RAG QA Logs & Corpus

This notebook treats the **RAG QA Logs & Corpus** as if it were telemetry from a real **RAG platform in production**.

The goal is to answer one practical question:

> *“If I owned this RAG system, what would I learn from its logs—and what decisions could I make?”*

It’s written in a **storytelling style** (not generic EDA) and focuses on **RAG operations, risk, and strategy** — with clean validation, slice-based diagnostics, and a simple confidence gate.

---

## 📌 What this notebook does

This notebook:

- ✅ Loads and validates the **multi-table RAG dataset** (documents, chunks, retrieval events, QA eval runs, scenarios).
- 🧷 Runs **integrity checks** (primary key uniqueness + join consistency) to prevent silent row blow-ups.
- 📊 Builds a **KPI snapshot** (correctness, hallucination risk, cost, latency) with **label coverage** awareness.
- 🗺️ Compares **corpus coverage vs question demand** by `domain` to spot “high-demand / low-coverage” areas.
- 🧩 Explores the **scenario landscape** (`scenario_type`, `difficulty`) to understand the traffic mix.
- 🔎 Produces **risk slices** (domain × scenario_type × difficulty) to prioritize **high-volume, low-correctness** segments.
- ⚙️ Compares **configurations** (retrieval strategy / generator model) via cost–quality trade-offs + Pareto frontier.
- 🧭 Separates failures into **retrieval/corpus** vs **generation/faithfulness** using a recall threshold split.
- 📈 Trains **one baseline LogisticRegression** model to estimate correctness from telemetry.
- 🚧 Simulates a **confidence gate** (threshold sweep) to trade off **coverage vs error rate**.
- 🧾 Includes **case files** (one likely-correct run + one risky run) with retrieved chunk snippets for human review.

Think of it as an **Ops & Analytics report** for a RAG system — not a playground notebook.

---

## 🧩 Dataset in use

The notebook expects the following CSV files to be available in the working directory (or a Kaggle input path):

- `rag_corpus_documents.csv`  
- `rag_corpus_chunks.csv`  
- `rag_qa_eval_runs.csv`  
- `rag_retrieval_events.csv`  
- `rag_qa_scenarios.csv`

Optional (only if present in your dataset export):

- `rag_qa_data_dictionary.csv`

All analysis is built on top of these linked tables. The notebook attempts to auto-locate them with `resolve_data_dir()`.

---

## 🧠 Notebook structure (high-level)

The notebook is organized into the following parts:

### 1️⃣ Setup & system picture

- Imports, configuration, helper functions (tables, callouts, KPI cards).
- A conceptual diagram of the RAG pipeline:

```text
        ┌────────────────┐      ┌─────────────────┐      ┌────────────────────────────┐
        │   Documents    │ ───▶ │     Chunks      │ ───▶ │   Retrieval (top-k list)   │
        └────────────────┘      └─────────────────┘      └────────────────────────────┘
                 ▲                        │                            │
                 │                        ▼                            ▼
         Corpus metadata         Retrieval events             QA eval runs (labels)
                 │                        │                            │
                 ▼                        ▼                            ▼
        Scenarios & use cases ─────────────────────────▶ System-level metrics & logs
```

- Data loading and **fast integrity checks**:
  - Primary key uniqueness checks: `doc_id`, `chunk_id`, `run_id`, `scenario_id`
  - Join consistency checks (e.g., chunks → docs, retrieval → chunks, retrieval → eval_runs, eval_runs → scenarios)

---

### 2️⃣ KPI snapshot + schema snapshot (trust the numbers)

- Schema scan: dtypes + missingness (optimized for quick scanning).
- KPI snapshot:
  - correctness rate (and label coverage)
  - hallucination rate (and label coverage)
  - average cost + p95 cost (if present)
  - average latency + p95 latency (if present)

📌 Important: rates are computed on labeled rows only — missing labels are not silently treated as negatives.

---

### 3️⃣ Corpus vs demand (coverage vs traffic)

- Compares:
  - document distribution by `domain`
  - eval-run distribution by `domain`
- Flags mismatches where eval traffic is high but corpus coverage is thin (index expansion / stricter routing candidates).

---

### 4️⃣ Scenario landscape (what users are asking)

- Scenario inventory by:
  - `scenario_type`
  - `difficulty` (renamed from `difficulty_level` when needed)
- Quick visualization of the top scenario types and how they distribute across difficulty levels.

---

### 5️⃣ 🗂️ Concrete case files (human-readable drill-downs)

- Samples:
  - one likely-correct run
  - one risky run (incorrect + hallucinated when possible)
- For each run, shows:
  - query + gold answer (if available)
  - labels, retrieval metrics, cost, latency
  - top retrieved chunks (rank/score/relevance + a readable snippet)

These are designed for demos, documentation, and dashboard drill-downs.

---

### 6️⃣ Quality, hallucinations & risk maps

- Base rate distributions for:
  - `is_correct`
  - `correctness_label` (if present)
  - `hallucination_flag`
  - `faithfulness_label` (if present)
- Per-domain views:
  - hallucination rate by domain
  - correctness label mix by domain (heatmap when available)
- Cross-tab correctness vs hallucination to see how often failures hallucinate.

---

### 7️⃣ Scenario breakdown (risk slices)

- Builds a slice table on labeled correctness:
  - `domain × scenario_type × difficulty`
- Prioritization rule:
  - **high volume + low correctness** = first to investigate

This section is your “where to fix first” map.

---

### 8️⃣ Strategy & economics (configuration trade-offs)

- Aggregates metrics by:
  - `retrieval_strategy`
  - `generator_model`
  - (optionally) `difficulty`
- Produces:
  - configuration league table (correctness / hallucination / latency / cost)
  - cost vs correctness scatter
  - Pareto frontier (best correctness at each cost level)

⚠️ The blended config “score” is a quick triage heuristic — Pareto frontier + slice sanity checks should guide decisions.

---

### 9️⃣ Retrieval vs generation (failure taxonomy)

- Uses `recall_at_10` and `is_correct` to split labeled runs into quadrants:

  - `good_retrieval_good_answer`
  - `good_retrieval_bad_answer`
  - `bad_retrieval_good_answer`
  - `bad_retrieval_bad_answer`

- This gives an actionable split between “retrieval/corpus problem” and “generation/faithfulness problem”.

Key knob:
- `RETRIEVAL_OK_THRESHOLD` controls the split; revisit if your recall definition changes.

---

### 🔟 Telemetry baseline model (early signal)

- Trains **one LogisticRegression** baseline to predict `is_correct` from:
  - retrieval metrics (`recall_at_k`, `mrr_at_10`, scores, n retrieved)
  - latency + cost
  - token counts (prompt/answer/context)
  - config metadata (`domain`, `task_type`, `difficulty`, `retrieval_strategy`, `generator_model`, …)

Evaluates:
- ROC-AUC + Average Precision
- Precision–Recall curve
- calibration curve (reliability diagram)
- confusion matrix (default threshold = 0.5)

The point is not perfection — it’s proving whether your logs contain **usable predictive signal**.

---

### 1️⃣1️⃣ 🚧 Confidence gate simulation (coverage vs error rate)

- Uses the model probability as a confidence score.
- Sweeps thresholds and computes:
  - **coverage** (fraction shown)
  - **error rate on shown answers**

This is the exact chart you need to discuss:
- safety targets
- product impact
- when to block / rerun / escalate

---
## 📦 What you get (outputs)

Running the notebook produces analysis-ready artifacts (tables + plots), including:

- ✅ Schema & missingness snapshot (all tables)
- ✅ Integrity checks (PK uniqueness + join consistency)
- ✅ KPI snapshot with label coverage awareness
- ✅ Corpus vs demand (domain distribution comparison)
- ✅ Scenario risk slices (domain × scenario_type × difficulty)
- ✅ Configuration trade-offs + Pareto frontier
- ✅ Retrieval vs generation quadrants (failure taxonomy)
- ✅ Baseline model evaluation (ROC/PR/calibration + confusion matrix)
- ✅ Confidence gate sweep (coverage vs error curve + threshold table)
---

## 🛠️ How to run

### Minimal requirements

- Python 3.9+
- Common data/ML stack:
  - `pandas`, `numpy`
  - `matplotlib`, `seaborn`
  - `scikit-learn`

### Local

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
jupyter lab
```

Open the notebook and run top-to-bottom.

### Kaggle

1. Add the **RAG QA Logs & Corpus** dataset as an input.
2. Run the notebook.
3. The notebook automatically searches under `/kaggle/input/...` to locate the CSVs.

---

## 🔁 How to reuse this notebook

You can reuse this notebook as:

- 🧪 A template for analyzing your own RAG telemetry exports.
- 🖥️ A starting point for a Streamlit “RAG Ops Monitor” (filters + drill-down + case files).
- 🎓 A teaching asset for RAG, failure taxonomy, and confidence gating.
- 📦 A benchmark notebook attached to the dataset on Kaggle / Hugging Face / GitHub.

---

## ✅ Key takeaways

- 🔎 Use scenario breakdowns to identify **high-volume slices with low correctness**.
- 🧭 Use retrieval-vs-answer taxonomy to decide whether failures are mostly **retrieval/corpus** or **generation/faithfulness**.
- ⚖️ Use config trade-offs (and Pareto frontier) to balance **quality, latency, and cost**.
- 🚧 Use threshold simulation to pick a confidence cutoff aligned with your **risk tolerance and desired coverage**.

---

## 🛣️ Next steps

- 🧰 Add interactive filters (domain, scenario_type, difficulty, configuration) for faster investigation.
- 💾 Export key slice tables (scenario breakdown, config summary, thresholds) as CSV artifacts for a dashboard layer.
- 📈 Re-run periodically to track drift and validate improvements after system changes.

---

## ✍️ Author

Author: Tarek Masryo
