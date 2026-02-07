from pathlib import Path

from ragqa.validation import validate_dataset


def test_validate_dataset_ok() -> None:
    data_dir = Path(__file__).parent / "data"
    rep = validate_dataset(data_dir)
    assert rep.required_ok is True
    assert rep.rows["rag_qa_eval_runs"] > 0
