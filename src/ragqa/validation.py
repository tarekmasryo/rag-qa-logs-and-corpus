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


def _assert_unique(df: pd.DataFrame, col: str, table: str) -> None:
    if col not in df.columns:
        raise KeyError(f"{table}: missing column '{col}'")
    dup = df[col].duplicated().sum()
    if dup:
        raise ValueError(f"{table}: '{col}' must be unique (duplicates={dup})")


def _assert_fk(left: pd.DataFrame, left_col: str, right: pd.DataFrame, right_col: str, name: str) -> None:
    if left_col not in left.columns:
        raise KeyError(f"{name}: missing left column '{left_col}'")
    if right_col not in right.columns:
        raise KeyError(f"{name}: missing right column '{right_col}'")

    left_vals = pd.Series(left[left_col].dropna().unique())
    right_set = set(right[right_col].dropna().unique())
    missing = [v for v in left_vals.tolist() if v not in right_set]
    if missing:
        sample = missing[:10]
        raise ValueError(f"{name}: foreign-key check failed. Missing sample={sample} (n_missing={len(missing)})")


def validate_dataset(data_dir: Path) -> ValidationReport:
    data_dir = data_dir.resolve()

    missing_required = [f for f in REQUIRED_FILES if not (data_dir / f).exists()]
    if missing_required:
        raise FileNotFoundError(f"Missing required files: {missing_required} in {data_dir}")

    present_optional = {f: (data_dir / f).exists() for f in OPTIONAL_FILES}

    documents = _read_csv(data_dir / "rag_corpus_documents.csv")
    chunks = _read_csv(data_dir / "rag_corpus_chunks.csv")
    scenarios = _read_csv(data_dir / "rag_qa_scenarios.csv")
    eval_runs = _read_csv(data_dir / "rag_qa_eval_runs.csv")

    # PK checks
    _assert_unique(documents, "doc_id", "rag_corpus_documents")
    _assert_unique(chunks, "chunk_id", "rag_corpus_chunks")
    _assert_unique(scenarios, "scenario_id", "rag_qa_scenarios")
    _assert_unique(eval_runs, "run_id", "rag_qa_eval_runs")

    # Join checks
    _assert_fk(chunks, "doc_id", documents, "doc_id", "chunks.doc_id -> documents.doc_id")
    _assert_fk(eval_runs, "scenario_id", scenarios, "scenario_id", "eval_runs.scenario_id -> scenarios.scenario_id")

    # Optional retrieval events
    if present_optional.get("rag_retrieval_events.csv"):
        retrieval = _read_csv(data_dir / "rag_retrieval_events.csv")
        # Many schemas exist; we validate chunk_id if present.
        if "chunk_id" in retrieval.columns:
            _assert_fk(retrieval, "chunk_id", chunks, "chunk_id", "retrieval_events.chunk_id -> chunks.chunk_id")

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
