from __future__ import annotations

import os
from pathlib import Path

REQUIRED_FILES: list[str] = [
    "rag_corpus_documents.csv",
    "rag_corpus_chunks.csv",
    "rag_qa_scenarios.csv",
    "rag_qa_eval_runs.csv",
]

OPTIONAL_FILES: list[str] = [
    "rag_retrieval_events.csv",
]


def _has_required(p: Path) -> bool:
    return all((p / f).exists() for f in REQUIRED_FILES)


def resolve_data_dir(arg_data_dir: str | None = None) -> Path:
    """Resolve the dataset directory.

    Priority:
    1) --data-dir argument
    2) RAGQA_DATA_DIR environment variable
    3) current working directory if it contains required files
    4) search under the current directory for required files (limited)
    """
    if arg_data_dir:
        p = Path(arg_data_dir).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"data_dir does not exist: {p}")
        return p

    env = os.getenv("RAGQA_DATA_DIR")
    if env:
        p = Path(env).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"RAGQA_DATA_DIR does not exist: {p}")
        return p

    here = Path.cwd().resolve()
    if _has_required(here):
        return here

    # Lightweight search: look for one required file and verify siblings
    # Avoid scanning huge trees.
    for marker in (REQUIRED_FILES[0], REQUIRED_FILES[2]):
        hits = list(here.rglob(marker))[:25]
        for h in hits:
            base = h.parent
            if _has_required(base):
                return base

    raise FileNotFoundError(
        "Could not locate required dataset CSVs. Put them in the working directory, "
        "pass --data-dir, or set RAGQA_DATA_DIR to the folder containing the required files."
    )
