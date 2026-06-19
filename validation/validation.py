import pandas as pd
def validate(Final_Result):
    df = pd.read_csv(Final_Result, sep="\t")

    print("CSV loaded successfully")
    print(df.head())

    errors = []
    indexError = 0

    #check at least 25 rows
    if len(df) < 25:
        printAndAppendError(errors, indexError, f"Row count validation failed: {len(df)} rows found, at least 25 required")
    else:
        print("Row count validation passed")

    # Required values
    required_columns = [
            "timestamp",
            "name",
            "raw_text_vosk",
            "time_taken_sec",
            "text",
            "question_flag",
            "num_words",
            "text_size_chars",
            "speech_rate_wps",
            "speaker_turn_id"
        ]
    existing_columns =  df.columns.intersection(required_columns).tolist()
    # [col for col in required_columns if col in df.columns]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        printAndAppendError(errors, indexError, f"Missing required columns: {', '.join(missing_columns)}")
    else:
        if df[existing_columns].isnull().values.any():
            printAndAppendError(errors, indexError, "Missing required values in the dataset")
        else:
            print("No missing required values")

    # check timestamp is a valid datetime
    if "timestamp" in df.columns:
        timestamp_check = pd.to_datetime(df["timestamp"], errors="coerce")

        for i, value in enumerate(timestamp_check, start=2):
            if pd.isna(value):
                printAndAppendError(errors, indexError, f"Row {i}: invalid timestamp value")

    # print all collected errors
    if errors:
        print("Validation failed:")
        for e in errors:
            print("-", e)
    else:
        print("No missing required values")
        print("Timestamp validation passed")

    # Numeric validation
    numeric_columns = [
            "time_taken_sec", 
            "num_words", 
            "speech_rate_wps", 
            "speaker_turn_id"
        ]

    for col in numeric_columns:
        if col in df.columns:
            if (df[col] <= 0).any():
                printAndAppendError(errors, indexError, f"{col} contains zero or negative values")
    # Boolean check
    if "question_flag" in df.columns:
        if not df["question_flag"].dropna().isin([True, False]).all():
            printAndAppendError(errors, indexError, "question_flag contains invalid values")

    # RESULT
    if errors:
        print("\nValidation Failed:\n")
        for e in errors:
            print("-", e)

    else:
        print("\nValidation Passed. Dataset is clean and ready for analysis!")



def printAndAppendError(errors, indexError, message):
    errors.append(message)
    print(errors[indexError])
    indexError += 1
    return indexError
