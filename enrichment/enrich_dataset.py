import pandas as pd

def enrich_dataframe(df):
    # Time: O(n) per operation - each apply iterates over n rows
    # Space: O(n) - new columns added to existing dataframe

    df["question_flag"] = df["text"].apply(
        lambda x: str(x).strip().endswith("?"))

    df["num_words"] = df["text"].apply(
        lambda x: len(str(x).split()))

    df["text_size_chars"] = df["text"].apply(
        lambda x: len(str(x)))

    df["speech_rate_wps"] = df.apply(
        lambda row: round(row["num_words"] / row["time_taken_sec"], 2)
        if row["time_taken_sec"] > 0 else 0, axis=1)

    # groupby is O(n), cumcount is O(n)
    df["speaker_turn_id"] = df.groupby("name").cumcount() + 1

    return df
