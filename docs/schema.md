# Dataset schema (quick reference)

This repo expects these CSVs (required filenames):

Required:
- `rag_corpus_documents.csv`
- `rag_corpus_chunks.csv`
- `rag_qa_scenarios.csv`
- `rag_qa_eval_runs.csv`

Optional:
- `rag_retrieval_events.csv` (enables deeper retrieval attribution)
- `docs/data_dictionary.csv` (human-friendly column descriptions)

The validation script checks:
- file presence (required)
- primary-key uniqueness (where applicable)
- key joins (chunks → documents, eval_runs → scenarios, retrieval_events → chunks when present)
