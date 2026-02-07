from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

REQUIRED_FILES: list[str] = [
    "rag_corpus_documents.csv",
    "rag_corpus_chunks.csv",
    "rag_qa_eval_runs.csv",
    "rag_qa_scenarios.csv",
]

OPTIONAL_FILES: list[str] = [
    "rag_retrieval_events.csv",
]


def _has_required(p: Path, required: Iterable[str] = REQUIRED_FILES) -> bool:
    return all((p / f).exists() for f in required)


def resolve_data_dir() -> Path:
    """Locate the folder containing the dataset CSVs.

    Order:
    1) env var `RAGQA_DATA_DIR`
    2) current working directory
    3) Kaggle: `/kaggle/input/<dataset>/`
    4) recursive search from cwd (anchor file)
    """

    env = os.environ.get("RAGQA_DATA_DIR")
    if env:
        p = Path(env).expanduser().resolve()
        if _has_required(p):
            return p
        raise FileNotFoundError(f"RAGQA_DATA_DIR set but required files not found in: {p}")

    here = Path(".").resolve()
    if _has_required(here):
        return here

    kaggle_root = Path("/kaggle/input")
    if kaggle_root.exists():
        for p in kaggle_root.iterdir():
            if p.is_dir() and _has_required(p):
                return p

        hits = list(kaggle_root.rglob(REQUIRED_FILES[2]))
        for h in hits[:25]:
            base = h.parent
            if _has_required(base):
                return base

    hits = list(here.rglob(REQUIRED_FILES[2]))
    for h in hits[:25]:
        base = h.parent
        if _has_required(base):
            return base

    raise FileNotFoundError(
        "Could not locate required dataset CSVs. Put them in the working directory, "
        "or set RAGQA_DATA_DIR to a folder that contains the required files."
    )
