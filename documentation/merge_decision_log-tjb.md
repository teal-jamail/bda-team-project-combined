# BDA Team Project — Notes

What this project is

A meeting recorder and speech analytics pipeline.
Five people sit together, each speakc short phrases into a mic
The app records, transcribes, corrects, enriches, validates, and analyses

Output: a CSV with 25+ rows and a printed analytics report

---

## The five stages

### Stage 1: Record and transcribe (vosk_transcription/)
Microphone casptures speech
Vosk converts audio to raw text file offline - no internet needed
Vosk is imperfect: no punctuation, mishears words, no capatalisation

Output: data/raw_transcript.csv

### Stage 2: AI correction (ai_correction/)
Ea. raw vosk transcript sent to Gemini for correction
Gemeni fixes spelling, add punctuation, keeps original meaning
If Gemini fails, Ollama is tried as a fallback
If both fail, the orgiginal raw text is kept unchanged

Output: data/correction_transcript.csv

### Stage 3: Enrichment (enrichment/)
Python calculates five new columns from corrected text
No AI - pure calculation
question_flag: does the text end with ?
num_words: how many words
text_size_chars: how many characters (w/ or w/o WS)
speech_rate_wps: words divided by seconds
speaker_turn_id: which turn number for speaker

Output: data/final_transcript.csv

### Stage 4: Validation (validation/)
Check final csv before analysis runs
Min. 25 rows, no missing values, correct types, valid ranges
Stops pipeline and prints errors if anything wrong

### Stage 5: Analytics (analysis/)
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

| Person | Stage | File                          |   Feeds into |
|--------|-------|------ -----------------|---------------------|
| Sergiu | 1 - Record | vosk_transcription/transcribe.py | Nita |
| Nita   | 2 - Correct | ai_correction/ollama_correct.py | Ebou |
| Ebou   | 3 - Enrich | enrichment/enrich_dataset.py | Alina |
| Alina  | 4 - Validate | validation/__init__.py | Teal |
| Teal   | 5 - Analyse | analyse/__init__.py | end output |

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


