from __future__ import annotations

import argparse
from pathlib import Path

from .io import resolve_data_dir
from .validation import validate_dataset


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate RAG QA Logs & Corpus dataset integrity.")
    p.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Folder containing the CSVs. If omitted, auto-detected (or via RAGQA_DATA_DIR).",
    )

    args = p.parse_args(argv)
    data_dir = Path(args.data_dir) if args.data_dir else resolve_data_dir()

    rep = validate_dataset(data_dir)
    print("OK: dataset validated")
    print(f"data_dir: {rep.data_dir}")
    for k, v in rep.rows.items():
        print(f"rows[{k}]: {v}")
    for f, ok in rep.optional_present.items():
        print(f"optional[{f}]: {'present' if ok else 'missing'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
