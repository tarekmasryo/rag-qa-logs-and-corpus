from __future__ import annotations

import os
from pathlib import Path

REQUIRED_FILES: list[str] = [
    "rag_corpus_documents.csv",
    "rag_corpus_chunks.csv",
    "eval_runs.csv",
    "scenarios.csv",
]

OPTIONAL_FILES: list[str] = [
    "rag_retrieval_events.csv",
    "data_dictionary.csv",
]

LEGACY_FILE_ALIASES: dict[str, list[str]] = {
    "eval_runs.csv": ["rag_qa_eval_runs.csv"],
    "scenarios.csv": ["rag_qa_scenarios.csv"],
}


def candidate_names(filename: str) -> list[str]:
    """Return canonical filename plus accepted legacy aliases."""
    return [filename, *LEGACY_FILE_ALIASES.get(filename, [])]


def find_dataset_file(data_dir: Path, filename: str) -> Path:
    """Resolve a dataset file by canonical name, allowing documented legacy aliases."""
    for candidate in candidate_names(filename):
        path = data_dir / candidate
        if path.exists():
            return path
    aliases = ", ".join(candidate_names(filename))
    raise FileNotFoundError(f"Missing required file in {data_dir}: expected one of [{aliases}]")


def has_dataset_file(data_dir: Path, filename: str) -> bool:
    return any((data_dir / candidate).exists() for candidate in candidate_names(filename))


def _has_required(path: Path) -> bool:
    return all(has_dataset_file(path, filename) for filename in REQUIRED_FILES)


def resolve_data_dir(arg_data_dir: str | None = None) -> Path:
    """Resolve the dataset directory.

    Priority:
    1) --data-dir argument
    2) RAGQA_DATA_DIR environment variable
    3) current working directory if it contains required files
    4) search under the current directory for required files (limited)
    """
    if arg_data_dir:
        path = Path(arg_data_dir).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"data_dir does not exist: {path}")
        return path

    env = os.getenv("RAGQA_DATA_DIR")
    if env:
        path = Path(env).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"RAGQA_DATA_DIR does not exist: {path}")
        return path

    here = Path.cwd().resolve()
    if _has_required(here):
        return here

    # Lightweight search: look for likely marker files and verify sibling files.
    # Avoid scanning huge trees.
    markers = ["rag_corpus_documents.csv", "scenarios.csv", "rag_qa_scenarios.csv"]
    for marker in markers:
        hits = list(here.rglob(marker))[:25]
        for hit in hits:
            base = hit.parent
            if _has_required(base):
                return base

    raise FileNotFoundError(
        "Could not locate required dataset CSVs. Put them in the working directory, "
        "pass --data-dir, or set RAGQA_DATA_DIR to the folder containing the required files."
    )
