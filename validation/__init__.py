import pandas as pd

def validate(Final_Result):
    #df = pd.read_csv(Final_Result, sep="\t")
    df = pd.read_csv(Final_Result)  #no separation between values as recording the data

    print("CSV loaded successfully")
    print(df.head())

    errors = []

    #check at least 25 rows
    if len(df) < 25:
        errors.append(f"Dataset has {len(df)} rows — minimum is 25.")
    else:
        print("Row count validation passed")

    # Required values
    required_columns = [
            "timestamp",
            "name",
            "raw_text_vosk",
            "text",
            "time_taken_sec",
            "num_words",
            "text_size_chars",
            "question_flag",
            "speech_rate_wps",
            "speaker_turn_id"
        ]
    existing_columns = [col for col in required_columns if col in df.columns]
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
    else:
        any_missing = False
        for index, row in df.iterrows():
            for col in existing_columns:
                value = row[col]
                if pd.isnull(value) or str(value).strip() == "":
                    print(f"Notice — Row {index + 2}: '{col}' is missing.")
                    any_missing = True
        if not any_missing:
            print("No missing required values")

    # check timestamp is a valid datetime
    if "timestamp" in df.columns:
        timestamp_check = pd.to_datetime(df["timestamp"], errors="coerce")

        for i, value in enumerate(timestamp_check, start=2):
            if pd.isna(value):
                errors.append(f"Row {i}: invalid timestamp value")


    # Numeric validation
    # num_words and speech_rate_wps might be equal to 0 when is silence, but negative makes no sense, 
    # so we split the numerical values into two parts- equal to 0 accepted, and non-negative accepted.
    
    strictly_positive_columns = ["time_taken_sec", "speaker_turn_id"] 
    non_negative_columns = ["num_words", "speech_rate_wps"]

    for col in strictly_positive_columns:
        if col in df.columns:
            if (df[col] <= 0).any():
                errors.append(f"{col} contains zero or negative values")

    for col in non_negative_columns:
        if col in df.columns:
            if (df[col] < 0).any():
                errors.append(f"{col} contains negative values")

    # Boolean check
    if "question_flag" in df.columns:
        if not df["question_flag"].dropna().isin([True, False]).all():
            errors.append("question_flag contains invalid values")

    # RESULT
    if errors:
        print("\nValidation Failed:\n")
        for e in errors:
            print("-", e)
        return False
    else:
        print("\nValidation Passed. Dataset is clean and ready for analysis!")
        return True
    

