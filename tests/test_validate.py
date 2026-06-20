import pandas as pd

from validation import REQUIRED_COLUMNS, validate


def _build_valid_dataframe(rows=25):
    data = {
        "timestamp": pd.date_range("2026-01-01", periods=rows, freq="s").astype(str),
        "name": ["Alice" if i % 2 == 0 else "Bob" for i in range(rows)],
        "raw_text_vosk": ["raw text"] * rows,
        "text": ["hello world"] * rows,
        "time_taken_sec": [1.0] * rows,
        "question_flag": ["True" if i % 2 == 0 else "False" for i in range(rows)],
        "num_words": [2] * rows,
        "text_size_chars": [11] * rows,
        "speech_rate_wps": [2.0] * rows,
        "speaker_turn_id": [i + 1 for i in range(rows)],
    }
    return pd.DataFrame(data, columns=REQUIRED_COLUMNS)


def test_validate_returns_true_for_valid_dataset(tmp_path, capsys):
    csv_path = tmp_path / "valid.csv"
    _build_valid_dataframe().to_csv(csv_path, index=False)

    result = validate(csv_path)

    captured = capsys.readouterr()
    assert result is True
    assert "Validation passed" in captured.out


def test_validate_returns_false_for_small_dataset_and_missing_columns(tmp_path, capsys):
    csv_path = tmp_path / "invalid.csv"
    df = _build_valid_dataframe(rows=5).drop(columns=["text"])
    df.to_csv(csv_path, index=False)

    result = validate(csv_path)

    captured = capsys.readouterr()
    assert result is False
    assert "Validation failed" in captured.out
    assert "minimum is 25" in captured.out
    assert "Missing required column: 'text'" in captured.out
