import pandas as pd

from analyse import analyse_dataset


def test_analyse_dataset_prints_expected_summary(tmp_path, capsys):
    csv_path = tmp_path / "analytics.csv"
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Alice", "Cara"],
            "num_words": [5, 3, 7, 2],
            "time_taken_sec": [10.0, 6.0, 14.0, 4.0],
            "question_flag": [True, False, True, False],
            "speech_rate_wps": [0.5, 0.5, 0.5, 0.5],
        }
    )
    df.to_csv(csv_path, index=False)

    analyse_dataset(csv_path)

    output = capsys.readouterr().out
    assert "Most words: Alice, 12 words" in output
    assert "Least words: Cara, 2 words" in output
    assert "Total speaking time: 34.0 seconds" in output
    assert "Most questions: Alice, 2 question(s)" in output
    assert "1. Alice: 24.0 seconds" in output
    assert "2. Bob: 6.0 seconds" in output
    assert "3. Cara: 4.0 seconds" in output
    assert "Alice: 0.5 words/second" in output
