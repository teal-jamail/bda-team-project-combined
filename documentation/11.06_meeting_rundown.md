========= 11.06 Overview =========
## Repo: teal-jamail/bda-team-project-combined

Hey all, here's the combined repo to share from single source.
Let's work from this going forward (instead of original repos 
[they have been preserved too])

--- 

## Setup

```bash
git clone https://github.com/teal-jamail/bda-team-project-combined.git
cd bda-team-project-combined
python3 -m venv .venv
source .venv/bin/activate
pip install pandas vosk sounddevice google-generativeai requests
```
* don't push 'venve/ folder to github or api keys


--- ## SERGIU ---

Your recording code is in 'vosk_transcription/transcribe.py`
Made couple annotions and light bug fix

Would you check that 'main.py' records and 
Please review the:
- `documentation/merge_decision_log-tjb.md`
- `code-walkthrough-tjb.md`
-- to see if any changes and reasoning look off


--- ## NITA ---

The pipeline architecture, folder structure, and implementation design 
form core of this project; super clean

Would you review and test the Ollama fallback
Please review the:
- `documentation/merge_decision_log-tjb.md`
- `code-walkthrough-tjb.md`
let me know if anything doesn't match what you had in mind.


--- ## Ebou ---

**Before the recording session:**
Read through documentation folder 
-- `merge_decision_log-tjb.md` and 
-- `code-walkthrough-tjb.md` 
for full picture of how everything connects

You're responsible for enrichment/enrich_dataset.py
The file is written and annoted on github
-- note the addition: 
a zero-guard on `time_taken_sec` to 
prevents division crash on bad data

This is your portion to explain in the video.

Would you write the complexity section for the README?
For each of the five operations, explain:
- what it does
- what n is in context
- why it is O(n)

**After the initial recording session:**

You're running data quality checks:
Once pipeline runs, check all three CSV files:

`data/raw_transcript.csv`
- timestamps, names, raw_text_vosk, time_taken_sec all populated

`data/correct_transcript.csv`
- text column looks like proper corrected English

`data/final_transcript.csv`
- question_flag is True or False per row
- num_words and text_size_chars are sensible numbers
- speech_rate_wps is a positive float
- speaker_turn_id counts correctly per speaker

flag anything that looks off

------- ** ALINA ---------

**Before recording session:**

Read through documentation folder 
-- `merge_decision_log-tjb.md` and 
-- `code-walkthrough-tjb.md` 
for full picture of how everything connects

Review your portion `validation/__init__.py` 
It checks six things:
- at least 25 rows in the dataset
- no missing values in required columns
- timestamp is a valid datetime
- time_taken_sec, num_words, speech_rate_wps, speaker_turn_id
  are numeric and greater than zero
- question_flag is True or False

This is your portion to explain in the video.

**After the initial recording session**

Once we have the real data, run it against the validation

```bash
python3 -c "from validation import validate; validate('data/final_transcript.csv')"
```

Check all of the errors and 
flag if anything fails 
-- nothing moves to analytics until validation complete

**Video:**

You're leading the recording and upload:
- record the team presenting
- ea. person speaks briefly about their contribution
- demo running pipeline on screen
- show  CSV, validation output, analytics output
- upload to OneDrive
- share with Stelios's email
- include the link in the peer evaluation form