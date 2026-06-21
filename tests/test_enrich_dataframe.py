import pandas as pd

from enrichment.enrich_dataset import enrich_dataframe


def test_enrich_dataframe_adds_expected_columns_and_values():
    df = pd.DataFrame(
        {
            "name": ["Alice", "Alice", "Bob"],
            "text": ["Hello world?", "No question", "Hi"],
            "time_taken_sec": [2.0, 4.0, 0.0],
        }
    )

    enriched = enrich_dataframe(df)

    assert enriched["question_flag"].tolist() == [True, False, False]
    assert enriched["num_words"].tolist() == [2, 2, 1]
    assert enriched["text_size_chars"].tolist() == [12, 11, 2]
    assert enriched["speech_rate_wps"].tolist() == [1.0, 0.5, 0]
    assert enriched["speaker_turn_id"].tolist() == [1, 2, 1]


def test_enrich_dataframe_mutates_and_returns_same_dataframe_object():
    df = pd.DataFrame(
        {
            "name": ["Alice"],
            "text": ["One line"],
            "time_taken_sec": [2.0],
        }
    )

    enriched = enrich_dataframe(df)

    assert enriched is df
