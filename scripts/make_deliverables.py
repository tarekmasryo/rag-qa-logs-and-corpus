from __future__ import annotations

import argparse
import json
from pathlib import Path

from ragqa.io import resolve_data_dir
from ragqa.validation import validate_dataset


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate a minimal validation deliverable JSON.")
    p.add_argument("--data-dir", type=str, default=None, help="Folder containing the CSVs.")
    p.add_argument("--out-dir", type=str, default="artifacts", help="Output folder (default: artifacts).")
    args = p.parse_args(argv)

    try:
        data_dir = resolve_data_dir(args.data_dir)
        rep = validate_dataset(Path(data_dir))
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}")
        return 2

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "data_dir": str(rep.data_dir),
        "required_ok": rep.required_ok,
        "rows": rep.rows,
        "optional_present": rep.optional_present,
    }
    (out_dir / "validation_report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote: {out_dir / 'validation_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
