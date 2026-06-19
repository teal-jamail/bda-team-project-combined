# BDA Team Project — Merge Decision Log

What this project is

A meeting recorder and speech analytics pipeline.
Five people sit together, each speakc short phrases into a mic
The app records, transcribes, corrects, enriches, validates, and analyses

Output: a CSV with 25+ rows and a printed analytics report

---


## Proposed changes pending (some merged 18.06) ~~(not merged as of 06.17)~~

### Nita Update 19/06
```markdown

**recording_session() — clean separation of concerns:**
- Speaker input fully moved out of transcribe.py into main.py as proposed.
- Empty name validation added — loop won't accept blank speaker name.
- Append-before-input pattern correct — independently got the last-turn fix right.

**ai_correction() — genuine upgrade over our version:**
Replaces simple `.apply(correct_with_fallback)` with a proper loop that:
- shows progress per row: [i/total_rows] Correcting: ...
- tracks which model was used per row (gemini/ollama/raw)
- returns source counts for a Stage 2 summary block:
  Gemini used: 18, Ollama used: 4, Raw used: 3
Worth keeping over what we had — adds transparency and is good for the demo video.

**correct_with_fallback() — refactored as a model loop:**
- Instead of nested try/except blocks, iterates over a list of (name, model) tuples
- Cleaner and easier to extend if a third model gets added.
- Now returns (corrected_text, source_name) instead of just corrected_text —
this is what feeds source_count tracking in ai_correction()

**transcribe.py — speaker input removed as planned:**
- record_turn(current_speaker) — no default None, no input() prompt inside.
- Speaker is always passed in from main.py
- Returns (phrase, duration) instead of (current_speaker, phrase, duration).
recognizer stays global for now
- noted this to consider moving inside the function for state isolation btwn turns

---

### Issues to fix before merging

**1 — wrong validation import (will crash immediately):**
```python
from validation.validation import validate  # Nita's branch
from validation import validate             # correct — our validate() is in __init__.py
```
- import looks for validation/validation.py which exists on Sergiu's branch
but not on main

**2 — analytics commented out:**
```python
# from analyse import analyse_dataset
# Stage 5 block fully commented out
```
analyse/__init__.py is now written and tested. Uncomment both the import and Stage 5
before merging.

**3 — return value mismatch between transcribe.py and main.py:**
- transcribe.py returns (phrase, duration) — two values.
- main.py correctly unpacks: phrase, time_taken_sec = record_turn(current_speaker)
- if either file gets merged without the other, any caller still expecting
(speaker, phrase, time_taken_sec) will crash with ValueError: not enough values to unpack.
- merge as a unit, not separately.


Don't merge transcribe.py without
simultaneously merging main.py — the return value contract changed.
```
---

## Sergiu's branch (origin/Sergiu) — reviewed, not safe to merge

### What changed

**transcribe.py:** essentially identical to main 
— record_turn(current_speaker=None)
w/ original three-value return (current_speaker, phrase, duration). 
- No incremental CSV write logic 

**validation/validation.py:** same file as already reviewed (Alina/Sergiu integration
attempt). Same bugs documented above — sep="\t", 25-row check commented out,
printAndAppendError index bug, no return True/False.

**main.py:** one new critical bug introduced

---

### Critical bug — append condition inverted

```python
if(not current_speaker):
    all_data.append({...})
else:
    print("No data recorded for this turn.")
```

`not current_speaker`:
- evaluates True only when current_speaker is None or empty.
- the code only appends when there is NO speaker name, and prints
"No data recorded for this turn" when there IS one.

- Every turn would be discarded. The pipeline would produce an empty
dataset every single run w/o any obvious error message. 
- serious invisible bug w/o actually running and checking the CSV output.

---

### Other issues (same as Nita's branch)

- `from validation.validation import validate` — wrong import path, will crash
- analytics import and Stage 5 both commented out
- validation/validation.py has the same bugs documented in Alina's validation review
  above — not safe to take from this branch


Dont merge-inverted append condition alone makes this branch unsafe —
it would produce empty datasets on every recording session.
transcribe.py adds nothing over main. Validation bugs already documented.

---

## CombinedBranch (origin/CombinedBranch)

### What improved over Sergiu's branch
- Inverted append condition fixed: if(current_speaker): is now correct
- 25-row check uncommented and active — only branch where this is restored

### Still broken
- sep="\t" still present — reads comma-separated files as tab-separated,
  breaks column alignment immediately on real data
- printAndAppendError index bug still present — indexError never updates
  in the caller, every live print shows errors[0] repeated
- no return True/False — is_valid always None, if not is_valid: always True,
  analytics blocked on every run regardless of actual data quality
- from validation.validation import validate — wrong import path, will crash
- analytics still commented out
- all_data.append() still after input() prompt — last-turn bug not fixed

### transcribe.py
Identical to Sergiu's branch and essentially our main version. Nothing new.

Closer than Sergiu's branch but still has three blockers preventing the pipeline
from running correctly. Do not merge.

---

## sergiu_with_main (origin/sergiu_with_main) 

### What improved
- all_data.append() moved before input() prompt — last-turn bug fixed

### New bugs introduced
- wrong import: from ai_correction.gemini_correct import ask_gemini_to_correct
  our function is ask_gemini — crashes immediately on import with ImportError
- "name": speaker in all_data.append() — speaker is undefined in this version,
  the name variable is current_speaker — crashes with NameError on first turn
- from validation.validation import validate — wrong import path
- analytics still commented out


Do not merge. Two new NameError/ImportError crashes introduced 
- The last-turn fix is correct but the surrounding code breaks in two other places

---

## teal-jamail-patch-1 (origin/teal-jamail-patch-1) — cleanest branch, closest to main

### What's there
- from validation import validate — correct import path 
- from analyse import analyse_dataset — correct import path 
- from ai_correction.gemini_correct import ask_gemini — correct 
- Stage 5 analytics fully restored and uncommented 
- essentially our main.py with the broken imports fixed — looks like a GitHub
  UI patch applied directly

### Still has issues
- all_data.append() still after input() prompt — last-turn bug present
  (already fixed on main, not carried over here)
- "name": current_speaker after the input update — if someone types a new
  name at the prompt, the current turn gets recorded under the new speaker's
  name rather than who just spoke (regression from the fix we applied to main)

### Moving Ahead
- All imports correct, analytics restored
- main already has the last-turn fix that this branch doesn't
Do not merge 
— main is already more correct
- Keep main as the base 
- use Nita's ai_correction() upgrade when three issues fixed (wrong validation import, analytics commented out, return value mismatch between transcribe.py and main.py).

---

## Overall

| Branch | Safe to merge | Key issue |
|--------|--------------|-----------|
| origin/nita | No — fix 3 issues first | Wrong validation import, analytics commented out, return value mismatch |
| origin/Sergiu | No | Inverted append condition — silently discards all data |
| origin/CombinedBranch | No | sep="\t", no return True/False, wrong import |
| origin/sergiu_with_main | No | ask_gemini_to_correct and speaker NameError crashes |
| origin/teal-jamail-patch-1 | No | Last-turn bug present, name regression |

Recommended path: keep main as bas
- Fix Nita's three issues on her branch,
- merge only her transcribe.py and main.py as a unit. 
Discard all other branches

---


### Alina's validation.py + Sergiu's integration attempt

Alina wrote a standalone validation script (AlinaM1994/bda-team-project,
validation.py) — not yet a callable function, runs as a script on import.
Uses vectorized timestamp check using pd.to_datetime(errors="coerce")
with enumerate(start=2) to map back to correct row numbers.

Bugs in her version:
- hardcoded "data.csv" filename with sep="\t" - wrong file, wrong separator
  (our pipeline writes comma-separated CSVs)
- no function wrapper - can't be imported/called by main.py
- row count check only prints, never appends to errors list - a <25 row
  dataset could still report "Validation Passed"

Sergiu attempted to integrate her version into his branch (teal-jamail/bda-team-project-combined, branch Sergiu, validation/validation.py).

Improvements: wrapped in def validate(Final_Result), cleaner column-intersection line. But:
- sep="\t" bug carried over unchanged - still breaks on real comma-separated data
- 25-row check now commented out entirely - disabled, not just buggy
(this is explcit project requirement)
- new printAndAppendError() helper has a reference bug: indexError is passed by value -- never updates in the caller
- -- every live print statement shows the first error repeated rather than the current one. 
- Final summary block is unaffected since it loops over errors directly.
- still no return True/False at the end - main.py's `if not is_valid:` would
  always evaluate True regardless of actual validation outcome, blocking
  every run unconditionally

Status: not safe to merge as-is. Alina is continuing to update her version
independently. Reconcile with whatever validate() currently exists in
validation/__init__.py at the Thursday meeting - need to confirm that file's
current state before comparing.

### Teal - last-turn bug in main.py
Fix: move all_data.append() to right after `record_turn()`, before `input()`
- smaller fix than serg's incremental-write approach
- doesnt change how the file gets written, protect in-memory list
- commented and pushed to main

- ~~the outer except KeyboardInterrupt only catches ctrl+C during `input()` prompt and not during record_turn() itself ["Press enter to continue or type new speaker name"]~~
- ~~that has its own internal handler in transcribe.py and returns normally~~
- ~~`all_data.appened()` currently after `input()`~~
- ~~if Ctrl+C at that prompt to end session, execution jumps to except before append runs; so that turns data would drop~~

---

### Sergiu's brach - incremental CSV writes + last-turn bug fix
- found edge case: when KeyboardInterrupt stops the recording loop, the last speakers turn wasnt being appended to all_data before exit
- checking against main.py/transcribe.py logic - may undercount rows

- change Stage 1's CSV write from one save at the end to incremental appends per turn: mode=`a`, header=False if file exists else True.

#### Tradeoff:
- both versions O(n) - all_data built either way since correction/enrichment need full df anyway
- currently: one to_csv() call, n rows written once - lower overhead
- proposed version: n seperate to_csv() calls, one per turn = extra overhead

- open question: is all_data still built in memory, or do later stages now read incrementally from disk

Naming flag: import says `ask_gemini_to_correct`, currently `ask_gemini`

---

### Nita's proposed restructure - speaker input ownership

- transcriby.py should only handle audio recording + speech-to-text (Vosk)
- should NOT handle speaker input
- main.py should fully merge speaker input with speaker changes

Contradicts current documentaiton: 
- record_turn(current_speaker=None) prompts for speaker name when current_speaker is None
- new version takes that out and moves all speaker logic to main.py
- leaves transcribe.py as purely audio and Vosk

How it improves:
- Seperation-of-concerns - recording logic doesnt need to know about user input

Status: Nita is now implementing this restructure directly rather than just
proposing it. transcribe.py and main.py will both change once pushed - review
needed at Thursday meeting before merging into main.
---

## What ea. person contributed

### Sergiu (diasergui/BDA_team_project)
Wrote first working pipeline: bda.py, vosk_microphone.py
gemeni_correct.py, process_raw_text.py, save_files.py, final_results.py

vosk_microphone.py - recording logic using sounddevice and Vosk
gemeni_correct.py - Gemeni API call, clean and correct

Code Issues:
- incorrect csv column names througout(name_speaker, raw_text. is_question)
- missing time_taken_sec and speech_rate_wps from the csv output
- count characters,but counted only letters, not full string ( wrong answer)
- speach_rate_wps typo - colum would have been named wrong in csv
- final_result.duration vs final_result.time_taken clash
- record_and_transcribe returned only final_raw_text, discarding full_text
- loop runs once per person - only 5 rows for 5 people, not 25

What was kept: vosk_microphone.py (w/ bug fix) and gemeni_correct.py
everything else updated

---
### itsNTM / Nita (itsNTM/bda_team_project)
Designed sophisticated pipeline archicture
Confirmed by notes.txt in repo 
- well-planned folder structure 
- 3-file audit trail
- Gemini-first-Ollama-fallback logic.
- Wrote main.py and shared

What was kept:complete architecture, main.py logic, enrich_dataframe

---

## Key decisions made during the merge

### Why the Pandas enrichment over Sergiu's process_raw_text.py
Sergiu's version: row-by-row inside the recording loop, incorrect column names, excluded white spaces and punctuation, only counted letters.

- if enrichment inside recording loop, its taking word count on raw Vosk txt b4 gemini correct; produing incorrect numbers from uncorrected
- pandas run on complete dataframe instead of row-by-row after the correction
- uses 'text' col. not 'raw_text_vosk

### Why correct_with_fallback over Sergiu's single Gemini Call
Sergiu's bda.py calls ask_gemini_to_correct() directly inside the loop
No error handling around it
If gemini fails mid-session - rate limit, network, API error - the whole run crashes and all recorded data lost
25 rows to record means multiple API calls - failure risk

Fallback chain in main.py:
1. try gemini first
2. if gemini fails, try ollama
3. if both fail, keep the original raw text unchanges
Recording sessions cannot be killed by an API failre

### Why KeyboardInterrupt over Sergiu's fixed headcount

bad.py: first prompts "how many team members speaking?"
for _ in range(number_of_team_members) - fixed loop
5 people = 5 rows - not enough for 25 min.

main.py: runs until Ctrl+C pressed
ea. person can speak as many turns as needed
session ends when team decides

* - : throwaway loop var. -repeats block n times, nvr used inside loop
* timestanp: strftime gives YMDHMS - more info than necessary [Nita uses isoformat() in bda.py]
* final-result.time_taken = duration: sets duration onto bj. after creation;
  process_raw_text then tries read back as final_result.duration [diff. name]
* attribution error at runtime - duration undefined on obj.
  fix: store everything in dict w/ consisten name (time_taken_sec) from start

---

## Team task assignments
Ea. person 1 stage

- Sergiu | 1 - Record | vosk_transcription/transcribe.py | Nita |
- Nita   | 2 - Correct | ai_correction/ollama_correct.py | Ebou |
- Ebou   | 3 - Enrich | enrichment/enrich_dataset.py | Alina |
- Alina  | 4 - Validate | validation/__init__.py | Teal |
- Teal   | 5 - Analyse | analyse/__init__.py | end output |

- integration - single repo: teal-jamail/bda-team-project-combined

##### Sergui's 
- dwnld vosk model locally (vosk-model-en-us-0.22-lgraph) since gitignored
- test 'record_turn()' works
- make sure 'sounddevice' installed [not pyaudio]

---

## CSV col. contract
** All files read/write same col. names in this exact order - please no renaming **

| Column          | Type    | Rule          |
|-----------------|---------|---------------|
| timestamp       | string  | ISO datetime  |
| name            | string  | not null      |
| raw_text_vosk   | string  | not null      |
| text            | string  | not null      |
| time_taken_sec  | float   | > 0           |
| question_flag   | boolean | True or False |
| num_words       | int     | > 0           |
| text_size_chars | int     | > 0           |
| speech_rate_wps | float   | > 0           |
| speaker_turn_id | int     | > 0           |

### Three files
- raw crashes → lose nada from correction or enrichment
- correction crashes → still have raw recording
- enrichment crashes → still have all 25 corrected rows

---

# The five stages

#### Stage 1: Record and transcribe (vosk_transcription/)
Microphone casptures speech
Vosk converts audio to raw text file offline - no internet needed
Vosk is imperfect: no punctuation, mishears words, no capatalisation

##### Output: data/raw_transcript.csv

---

#### Stage 2: AI correction (ai_correction/)
Ea. raw vosk transcript sent to Gemini for correction
Gemeni fixes spelling, add punctuation, keeps original meaning
If Gemini fails, Ollama is tried as a fallback
If both fail, the orgiginal raw text is kept unchanged

##### Output: data/correction_transcript.csv

---

#### Stage 3: Enrichment (enrichment/)
Python calculates five new columns from corrected text
No AI - pure calculation
question_flag: does the text end with ?
num_words: how many words
text_size_chars: how many characters (w/ or w/o WS)
speech_rate_wps: words divided by seconds
speaker_turn_id: which turn number for speaker

##### Output: data/final_transcript.csv

---

#### Stage 4: Validation (validation/)
Check final csv before analysis runs
Min. 25 rows, no missing values, correct types, valid ranges
Stops pipeline and prints errors if anything wrong

---

#### Stage 5: Analytics (analysis/)
Answers six question about the meeting using pandas
Who spoke most/least, total time, avg. time, most questions
top 5 speakers by time (+ # of tunrs?); avg. speech rate per speaker

---

## Folder sturcture and why

- vosk_transcription/ - Stage 1 
- ai_correction/      - Stage 2
- enrichment/         - Stage 3
- validation/         - Stage 4
- analysis/           - Stage 5
- common/             - shared untilities (load.csv, save_csv)
- data/               - csv file from pipline (gitignored)

Reason for seperation: each stage has a job
A bug in enrichment can't affect transcription
Two peopl can work on different stages w/o git conflicts
"Seperation of concerns"