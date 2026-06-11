import pandas as pd

def enrich_dataframe(df):
    # takes csv as df from helpers pd conversion

    # Time: O(n) per operation - each apply iterates over n rows
    # Space: O(n) - new columns added to existing dataframe

    df["question_flag"] = df["text"].apply(
        lambda x: str(x).strip().endswith("?"))
        # returns questions
        # 'str(x)': safety conversion
        # even though 'text' col. SHOULD be only str, 
        # pd sometimes reads vals as 'float' [esp. NaN or missing]
        # '.strip()': onto a NaN give AttributionError
        # wrap in 'str(x)' converts everything to str b4 strips

    df["num_words"] = df["text"].apply(
        lambda x: len(str(x).split()))
        # returns num. words
        # splits on any ws AND handles multiple spaces b/t words

    df["text_size_chars"] = df["text"].apply(
        lambda x: len(str(x)))
        # returns num. characters
        # len(str(x)) counts everything - letters, spaces commas, etc.

    df["speech_rate_wps"] = df.apply(
        lambda row: round(row["num_words"] / row["time_taken_sec"], 2)
        if row["time_taken_sec"] > 0 else 0, axis=1)
        # returns speeach rate in wps
        # axis=1 apply func. across ea. row
        # guard: if time_taken_sec is 0 or nul -->
        # return 0 instead of attempting division

    # groupby is O(n), cumcount is O(n)
    df["speaker_turn_id"] = df.groupby("name").cumcount() + 1
    # groups above by speaker name and 
    # cumcount shows how many times spoke
    # +1 shift to start at 1 instead of 0

    return df
