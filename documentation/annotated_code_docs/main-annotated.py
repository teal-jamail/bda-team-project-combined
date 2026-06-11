
# seperation of concerns: ea. import pulls one function from one module
# pipline stages ea. represent a single function
# main.py is the orchestration layer

from vosk_transcription.transcribe import record_turn
from ai_correction.gemini_correct import ask_gemini
from ai_correction.ollama_correct import ask_ollama
from enrichment.enrich_dataset import enrich_dataframe
from validation import validate
from analyse import analyse_dataset
from common.helpers import load_csv, save_csv
from datetime import datetime
import pandas as pd

# Three files:

RAW_FILE = "data/raw_transcript.csv"
# - raw crashes → lose nada from correction or enrichment

CORRECT_FILE = "data/correct_transcript.csv"
# - correction crashes → still have raw recording

FINAL_FILE = "data/final_transcript.csv"
# - enrichment crashes → still have all 25 corrected rows

# if need change file path do it in one place rather than hunt throughcode3

def correct_with_fallback(text):
    # Try Gemini first

    # fallback chain: gemini -> Ollama -> org. txt
    # recording cannot be killed by api failure

    try:
        result = ask_gemini(text)
        if result:
            return result
            # if gemeini returns corrected txt, use and stop here

    except Exception as e:
        print("Gemini failed:", e)
        # catches gemini error (rate limit, network, invalid key)
        # gives/stores error a name 'e' to print what went wrong
        # Fallback to Ollama

    try:
        result = ask_ollama(text)
        if result:
            return result
            # if ollama returns corrected txt, use and stop here
   
    except Exception as e:
        # catch ollama error (server not running, model not pulled)
        # execution cont'd until final fallback

        print("Ollama failed:", e)
        # Final fallback both fail: return original text unchanged
        # pipeline cont'd, correction gets raw vosk

    print("Both AI corrections failed, keeping original.")
    return text


def main():
    print("\n=============== Team Meeting Recorder Started ===============\n")

    # ====== Stage 1: Record and transcribe ======

    all_data = []
    # create new df w/ all data
    current_speaker = None
    # signals prompt for speaker

    try:
        while True:
            speaker, phrase, time_taken_sec = record_turn(current_speaker)
            # if speaker, phrase, duration present save as new df 'record_turn' with speaker_name

            change = input("\nPress ENTER to continue or type new speaker name: ").strip()
            current_speaker = change if change else speaker
            # ternary: if user input new name use
            # if pressed 'enter' keep current speaker
            # allows multiple turns per person or switch new speaker
            
            all_data.append({
                "timestamp": datetime.now().isoformat(),
                # captured after completed turn - marks when turn happened
                # per turn not total session
                "name": current_speaker,
                "raw_text_vosk": phrase,
                "time_taken_sec": time_taken_sec
            })

    except KeyboardInterrupt:
        print("\nRecording stopped.")
        # w/o except program crash w/ KeyboardInterrupt
        # here marks and execution continues

    if not all_data:
        print("No data recorded.")
        return
        # guard: if KeyboardInterrupt fired immediately w/o recording
        # empty list would create blank df
        # pipeline would run nothing & fail validation
        # return exits cleanly

    df = pd.DataFrame(all_data)
    # list of dicts; one dict per term
    # converts to list into table - ea. dict key becomes col.
    # ea. dict becomes a row

    save_csv(df, RAW_FILE)
    # if anything crashes in stage 2/3: retains raw recordings
    print(f"\nStage 1 complete: {len(df)} rows saved to {RAW_FILE}")

    # ====== Stage 2: AI correction ======
    print("\nStarting AI correction...\n")
    correct_df = df.copy()
    # creates independent copy

    correct_df["text"] = correct_df["raw_text_vosk"].apply(correct_with_fallback)
    # gets new 'text' col. added w/o affecting original df
    # calls 'correct_with_fallback 1x for ea. row in raw_text_vosk col.
    # passes ea. raw trans. thru fallback 1 at a time
    # corrected result saved in new 'text' col.

    save_csv(correct_df, CORRECT_FILE)
    # saves corrected df from post-fallback pipeline push
    # if crash correct data still safe
    # cost is high : 1 API call per row

    print(f"Stage 2 complete: corrected transcript saved to {CORRECT_FILE}")
    # prints row count confirmation

    # ====== Stage 3: Enrichment ======
    print("\nEnriching dataset...\n")
    
    final_df = enrich_dataframe(correct_df)
    # pass 'correct_df' to enrich - adds 5 calculated cols.
    # enrichment read from 'text' col. only found in 'correct_df'
    # returns enriched df and stores as final_df

    save_csv(final_df, FINAL_FILE)
    # two args.: df & filepath
    # writes final_df w/ enriched df w/ all 10 cols. to 'data/final_transcript.csv'
    # validation & analytics will read from 
    
    print(f"Stage 3 complete: enriched dataset saved to {FINAL_FILE}")


    # ====== Stage 4: Validation ======
    print("\nRunning validation...\n")
    
    is_valid = validate(FINAL_FILE)
    # validate is boolean t/f
    # goes to stage 5 if True

    if not is_valid:
        # if return False prints error and execution stops
        print("\nFix validation errors before continuing.")
        return


    # ====== Stage 5: Analytics ======
    print("\nRunning analytics...\n")
    analyse_dataset(FINAL_FILE)
    # answers 6 questions & prints to console

if __name__ == "__main__":
    main()
