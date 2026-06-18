import pandas as pd

REQUIRED_COLUMNS = [
    "timestamp", "name", "raw_text_vosk", "text",
    "time_taken_sec", "question_flag", "num_words",
    "text_size_chars", "speech_rate_wps", "speaker_turn_id"
]

def validate(filepath):
    # Time: O(n) - checks every row for every condition
    # Space: O(n) - loads full dataframe into memory
    df = pd.read_csv(filepath)
    errors = []

    if len(df) < 25:
        errors.append(f"Dataset has {len(df)} rows — minimum is 25.")

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing required column: '{col}'")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"  - {e}")
        return False

    for i, row in df.iterrows():
        row_num = i + 2

        for col in REQUIRED_COLUMNS:
            if pd.isnull(row[col]) or str(row[col]).strip() == "":
                errors.append(f"Row {row_num}: '{col}' is missing.")

        try:
            pd.to_datetime(row["timestamp"])
        except Exception:
            errors.append(f"Row {row_num}: timestamp '{row['timestamp']}' is not a valid datetime.")

        for col in ["time_taken_sec", "num_words", "speech_rate_wps", "speaker_turn_id"]:
            try:
                val = float(row[col])
                if val <= 0:
                    errors.append(f"Row {row_num}: '{col}' must be greater than 0, got {val}.")
            except (ValueError, TypeError):
                errors.append(f"Row {row_num}: '{col}' is not numeric.")

        if str(row["question_flag"]).strip() not in ["True", "False", "true", "false"]:
            errors.append(f"Row {row_num}: 'question_flag' must be True or False, got '{row['question_flag']}'.")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(f"  - {e}")
        return False

    print(f"Validation passed: {len(df)} rows, all checks passed.")
    return True