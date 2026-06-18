from vosk_transcription.transcribe import record_turn
from ai_correction.gemini_correct import ask_gemini
from ai_correction.ollama_correct import ask_ollama
from enrichment.enrich_dataset import enrich_dataframe
from validation.validation import validate
# from analyse import analyse_dataset
from common.helpers import load_csv, save_csv
from datetime import datetime
import pandas as pd


RAW_FILE = "data/raw_transcript.csv"
CORRECT_FILE = "data/correct_transcript.csv"
FINAL_FILE = "data/final_transcript.csv"


def correct_with_fallback(text):

    try:
        result = ask_gemini(text)
        if result:
            return result

    except Exception as e:
        print("Gemini failed:", e)


    try:
        result = ask_ollama(text)
        if result:
            return result
   
    except Exception as e:

        print("Ollama failed:", e)

    print("Both AI corrections failed, keeping original.")

    return text


def main():
    print("\n=============== Team Meeting Recorder Started ===============\n")

    # ====== Stage 1: Record and transcribe ======

    all_data = []
    current_speaker = None

    try:
        while True:
            current_speaker, phrase, time_taken_sec = record_turn(current_speaker)
            if(current_speaker):
                all_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "name": current_speaker,
                    "raw_text_vosk": phrase,
                    "time_taken_sec": time_taken_sec
                })
            else:
                print("No data recorded for this turn.")


            change = input("\nPress ENTER to continue or type new speaker name: ").strip()
            current_speaker = change if change else current_speaker

            

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    if not all_data:
        print("No data recorded.")
        return

    df = pd.DataFrame(all_data)
    save_csv(df, RAW_FILE)

    print(f"\nStage 1 complete: {len(df)} rows saved to {RAW_FILE}")

    # ====== Stage 2: AI correction ======
    print("\nStarting AI correction...\n")
    
    correct_df = df.copy()
    correct_df["text"] = correct_df["raw_text_vosk"].apply(correct_with_fallback)
    save_csv(correct_df, CORRECT_FILE)

    print(f"Stage 2 complete: corrected transcript saved to {CORRECT_FILE}")


    # ====== Stage 3: Enrichment ======
    print("\nEnriching dataset...\n")
    
    final_df = enrich_dataframe(correct_df)

    save_csv(final_df, FINAL_FILE)
    
    print(f"Stage 3 complete: enriched dataset saved to {FINAL_FILE}")


    # ====== Stage 4: Validation ======
    print("\nRunning validation...\n")
    
    is_valid = validate(FINAL_FILE)

    if not is_valid:

        print("\nFix validation errors before continuing.")
        return


    # # ====== Stage 5: Analytics ======
    # print("\nRunning analytics...\n")
    # analyse_dataset(FINAL_FILE)


if __name__ == "__main__":
    main()
