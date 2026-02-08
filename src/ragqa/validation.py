from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .io import OPTIONAL_FILES, REQUIRED_FILES


@dataclass(frozen=True)
class ValidationReport:
    data_dir: Path
    required_ok: bool
    optional_present: dict[str, bool]
    rows: dict[str, int]


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _assert_unique(df: pd.DataFrame, col: str, name: str) -> None:
    if col not in df.columns:
        raise ValueError(f"Missing required column '{col}' in {name}")
    if not df[col].is_unique:
        dup = df[col][df[col].duplicated()].head(5).tolist()
        raise ValueError(f"Column '{col}' must be unique in {name}. Example duplicates: {dup}")


def _assert_fk(
    child: pd.DataFrame,
    child_col: str,
    parent: pd.DataFrame,
    parent_col: str,
    relation: str,
) -> None:
    if child_col not in child.columns:
        raise ValueError(f"Missing FK column '{child_col}' in {relation}")
    if parent_col not in parent.columns:
        raise ValueError(f"Missing PK column '{parent_col}' in {relation}")
    missing = set(child[child_col].dropna().unique()) - set(parent[parent_col].dropna().unique())
    if missing:
        ex = list(sorted(missing))[:5]
        raise ValueError(f"Broken FK {relation}. Example missing keys: {ex}")


def validate_dataset(data_dir: Path) -> ValidationReport:
    """Validate multi-table dataset integrity for RAG QA Logs & Corpus.

    Checks:
    - required files exist
    - primary-key uniqueness (doc_id, chunk_id, scenario_id, run_id)
    - FK joins (chunks.doc_id -> documents.doc_id, eval_runs.scenario_id -> scenarios.scenario_id)
    - optional retrieval FK checks when rag_retrieval_events.csv exists
    """
    data_dir = Path(data_dir).expanduser().resolve()

    missing_files = [f for f in REQUIRED_FILES if not (data_dir / f).exists()]
    if missing_files:
        raise FileNotFoundError(f"Missing required files in {data_dir}: {missing_files}")

    present_optional = {f: (data_dir / f).exists() for f in OPTIONAL_FILES}

    documents = _read_csv(data_dir / "rag_corpus_documents.csv")
    chunks = _read_csv(data_dir / "rag_corpus_chunks.csv")
    scenarios = _read_csv(data_dir / "rag_qa_scenarios.csv")
    eval_runs = _read_csv(data_dir / "rag_qa_eval_runs.csv")

    # Primary keys
    _assert_unique(documents, "doc_id", "rag_corpus_documents.csv")
    _assert_unique(chunks, "chunk_id", "rag_corpus_chunks.csv")
    _assert_unique(scenarios, "scenario_id", "rag_qa_scenarios.csv")
    _assert_unique(eval_runs, "run_id", "rag_qa_eval_runs.csv")

    # Foreign keys
    _assert_fk(chunks, "doc_id", documents, "doc_id", "chunks.doc_id -> documents.doc_id")
    _assert_fk(eval_runs, "scenario_id", scenarios, "scenario_id", "eval_runs.scenario_id -> scenarios.scenario_id")

    # Optional: retrieval events
    if present_optional.get("rag_retrieval_events.csv"):
        retrieval = _read_csv(data_dir / "rag_retrieval_events.csv")
        if "chunk_id" in retrieval.columns:
            _assert_fk(retrieval, "chunk_id", chunks, "chunk_id", "retrieval_events.chunk_id -> chunks.chunk_id")
        # If example_id exists in both, validate it (best-effort)
        if "example_id" in retrieval.columns and "example_id" in eval_runs.columns:
            missing = set(retrieval["example_id"].dropna().unique()) - set(eval_runs["example_id"].dropna().unique())
            if missing:
                ex = list(sorted(missing))[:5]
                raise ValueError(f"Broken FK retrieval_events.example_id -> eval_runs.example_id. Example missing: {ex}")

    rows = {
        "rag_corpus_documents": len(documents),
        "rag_corpus_chunks": len(chunks),
        "rag_qa_scenarios": len(scenarios),
        "rag_qa_eval_runs": len(eval_runs),
    }

    return ValidationReport(
        data_dir=data_dir,
        required_ok=True,
        optional_present=present_optional,
        rows=rows,
    )
