from vosk_transcription.transcribe import record_turn
from ai_correction.gemini_correct import ask_gemini
from ai_correction.ollama_correct import ask_ollama
from enrichment.enrich_dataset import enrich_dataframe
from validation import validate
from analyse import analyse_dataset
from common.helpers import load_csv, save_csv
import time
import os
from datetime import datetime
import pandas as pd

RAW_FILE = "data/raw_transcript.csv"
CORRECT_FILE = "data/correct_transcript.csv"
FINAL_FILE = "data/final_transcript.csv"

def recording_session():
    all_data = []
    current_speaker = input("Enter speaker name: ").strip()

    while not current_speaker:
        current_speaker = input("Speaker cannot be empty. Enter name: ").strip()

    try:
        while True:
            phrase, time_taken_sec = record_turn(current_speaker)
            all_data.append({
                "timestamp": datetime.now().isoformat(),
                "name": current_speaker,
                "raw_text_vosk": phrase,
                "time_taken_sec": time_taken_sec
            })
            
            # old prompt: change = input("Press ENTER or type new speaker name: ").strip()
            # replaced with explicit 'done' exit to avoid Ctrl+C ambiguity
            change = input("Press ENTER for same speaker, type name to switch, or type 'done' to finish: ").strip()
            
            if change.lower() == "done": # change lowercase so all dunctions same
                break                    # exits the `while ture` loop
                
            current_speaker = change or current_speaker
            # only runs when `done` is not types 
            # if new user name input `current_speaker` becomes new name (T)
            # if press enter change is empty str (F)

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    return all_data

def correct_with_fallback(text):

    models = [
        ("gemini", ask_gemini),
        ("ollama", ask_ollama)
    ]

    for name, model in models:
        try:
            result = model(text)
            if result and result.strip():
                return result.strip(), name
        except Exception as e:
            print(f"{name.capitalize()} failed: {e}")

    print("Both AI corrections failed, keeping original.")

    return text, "raw"

def ai_correction(df):

    correct_df = df.copy()

    texts = []

    source_count = {
        "gemini": 0,
        "ollama": 0,
        "raw": 0
    }

    text_row = correct_df["raw_text_vosk"].fillna("")
    total_rows = len(text_row)

    for i, text in enumerate(text_row, start=1):

        print(f"\n[{i}/{total_rows}] Correcting: {str(text)[:40]}...")

        corrected, source = correct_with_fallback(text)

        texts.append(corrected)

        source_count[source] += 1

        print(f"Source used: {source}")
        # time.sleep(13) # stay under 5 requests per min. [free tier limit]

    correct_df["text"] = texts

    return correct_df, total_rows, source_count

def main():
    print("\n=============== Team Meeting Recorder Started ===============\n")

    # ====== Stage 1: Record and transcribe ======
    if os.path.exists(RAW_FILE):
        # skip recording if raw csv already exists
        # protects overwrites
        # useful only for re-run correction or enrichment

        print(f"Raw transcript found at {RAW_FILE} — skipping recording.")
        df = pd.read_csv(RAW_FILE)
        # Time: O(n) - n rows from disk
        # Space: O(n) - load full data to memory

    else:
        # no raw csv found - run the full recording sesh
        all_data = recording_session()
        if not all_data:
            print("No data to re-record.")
            return
            # guard: exits if session empty
        df = pd.DataFrame(all_data)
        # converts list of dicts to df - 1 dict per turn

        save_csv(df, RAW_FILE)
        print(f"\nStage 1 complete: {len(df)} rows saved to {RAW_FILE}")
    
    # ====== Stage 1: Record and transcribe ======

    # all_data = recording_session()

    # if not all_data:
        # print("No data recorded.")
        # return

    # df = pd.DataFrame(all_data)

    # save_csv(df, RAW_FILE)

    # print(f"\nStage 1 complete: {len(df)} rows saved to {RAW_FILE}")

   
   # ====== Stage 2: AI correction ======
    if os.path.exists(CORRECT_FILE):
    # skip correction if corrected csv already exists
    # avoids rerunning 25+ API calls unnecessarily

        print(f"Corrected transcript at {CORRECT_FILE} — skipping correction.")
        correct_df = pd.read_csv(CORRECT_FILE)

    else:
        print("\nStarting AI correction...\n")
        correct_df, total_rows, source_count = ai_correction(df)
        save_csv(correct_df, CORRECT_FILE)
        print(f"Stage 2 complete: corrected transcript saved to {CORRECT_FILE}")
   

    # ====== Stage 2: AI correction ======
    # print("\nStarting AI correction...\n")

    # correct_df, total_rows, source_count = ai_correction(df)

    # save_csv(correct_df, CORRECT_FILE)

    # print(f"Stage 2 complete: corrected transcript saved to {CORRECT_FILE}")

    print("\n============================== SUMMARY ==============================")
    print(f"Processed rows: {total_rows}")
    print(f"Gemini used: {source_count['gemini']}")
    print(f"Ollama used: {source_count['ollama']}")
    print(f"Raw used: {source_count['raw']}")
    print("======================================================================\n")

    # ====== Stage 3: Enrichment ======
    if os.path.exists(FINAL_FILE):
        # skip enrichment if final CSV already exists
        print(f"Final transcript found at {FINAL_FILE} — skipping enrichment.")
        final_df = pd.read_csv(FINAL_FILE)
    else:
        print("Enriching dataset...\n")
        final_df = enrich_dataframe(correct_df)
        save_csv(final_df, FINAL_FILE)
        print(f"Stage 3 complete: enriched dataset saved to {FINAL_FILE}")

    # ====== Stage 3: Enrichment ======
    # print("\nEnriching dataset...\n")
    
    # final_df = enrich_dataframe(correct_df)

    # save_csv(final_df, FINAL_FILE)
    
    # print(f"Stage 3 complete: enriched dataset saved to {FINAL_FILE}")


    # ====== Stage 4: Validation ======
    print("\nRunning validation...\n")
    
    is_valid = validate(FINAL_FILE)

    if not is_valid:

        print("\nFix validation errors before continuing.")
        return


<<<<<<< HEAD
    # # ====== Stage 5: Analytics ======
=======
    # ====== Stage 5: Analytics ======
>>>>>>> 4896b702e68121b94f436126bdca2f4d4774c749
    print("\nRunning analytics...\n")
    analyse_dataset(FINAL_FILE)


if __name__ == "__main__":
    main()