# Dataset schema quick reference

This repository expects a multi-table RAG QA evaluation dataset.

## Required files

```text
rag_corpus_documents.csv
rag_corpus_chunks.csv
eval_runs.csv
scenarios.csv
```

## Recommended optional files

```text
rag_retrieval_events.csv
data_dictionary.csv
```

`rag_retrieval_events.csv` enables deeper retrieval attribution. `data_dictionary.csv` is used by the notebook as a human-readable schema helper when available.

## Core keys

| Table | Primary key / important key | Notes |
|---|---|---|
| `rag_corpus_documents.csv` | `doc_id` | One row per source document. |
| `rag_corpus_chunks.csv` | `chunk_id` | Each chunk should reference `doc_id`. |
| `scenarios.csv` | `scenario_id` | Scenario metadata such as domain/type/difficulty. |
| `eval_runs.csv` | `run_id` | Evaluation rows should reference `scenario_id`. |
| `rag_retrieval_events.csv` | varies | Should reference `chunk_id`; may reference `example_id` when available. |

## Validation checks

The CLI checks:

- required file presence,
- required columns for key checks,
- primary-key uniqueness,
- `rag_corpus_chunks.doc_id -> rag_corpus_documents.doc_id`,
- `eval_runs.scenario_id -> scenarios.scenario_id`,
- `rag_retrieval_events.chunk_id -> rag_corpus_chunks.chunk_id` when retrieval events exist,
- `rag_retrieval_events.example_id -> eval_runs.example_id` when both columns exist.

## Legacy filename aliases

For compatibility, the CLI also accepts these older filenames:

| Current filename | Legacy alias |
|---|---|
| `eval_runs.csv` | `rag_qa_eval_runs.csv` |
| `scenarios.csv` | `rag_qa_scenarios.csv` |
