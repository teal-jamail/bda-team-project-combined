# BDA Team Project — Code Walkthrough
---

## Code breakdown by stage

### Stage 1:
- `all_data`: list of dicts, one per turn
- `current_speaker=None`: signals prompt on first call
- ternary: keeps current speaker or switches if new name typed
- timestamp captured per turn after recording completes
- `KeyboardInterrupt` caught cleanly, execution continues
- guard: empty `all_data` exits before creating blank dataframe
- `pd.DataFrame(all_data)`: converts list of dicts to table
- saved immediately: raw recordings protected before API calls begin

### Stage 2:
- `df.copy()`: independent copy so raw df stays untouched
- `.apply(correct_with_fallback)`: one API call per row, O(n)
- saved immediately: corrected data protected before enrichment

### Stage 3:
- `correct_df` passed in: enrich reads from `text` col. only in `correct_df`
- `enrich_dataframe` adds five calculated columns, returns modified df
- saved as `FINAL_FILE`: read by validation and analytics

### Stage 4:
- `validate` returns True or False
- if False: prints errors and `return` stops pipeline completely
- no analytics on broken data

### Stage 5:
- one line: answers six questions, prints to console
- no save, no return value needed
  
---

## File walkthrough

### ai_correction/ollama_correct.py

Sends raw Vosk txt to local Ollama server for correction.
Ollama runs locally (http://localhost:11434) - no internet needed.

#### imports:
- `requests`: sends HTTP request to local Ollama server

#### constants (defined once for reuse):
- `MODEL_NAME`: uses gemma3
- `OLLAMA_URL`: address of local Ollama API endpoint

#### ask_ollama(prompt):
- posts prompt to Ollama w/ `stream:False` (full response, not token-by-token)
- `raise_for_status()`: error handling - stops if server returns error code
- returns corrected txt stripped of extra ws

#### if __name__ == "__main__":
- test block - runs only when file directly executed
- doesn't run when main.py imports ask_ollama
- can test Ollama works w/o running full pipeline

---

### vosk_transcription/transcribe.py

Records one speaker turn via mic and returns transcript and duration.
Uses Vosk for offline speech-to-text - no internet needed.

#### imports:
- `json`: Vosk returns JSON strings, `json.loads()` converts to dict
- `queue`: thread-safe queue, mic runs in one thread, Vosk processes in another
- `sounddevice`: captures raw audio from mic as stream
- `vosk Model`: loads speech recognition model from disk
- `vosk KaldiRecognizer`: speech-to-text conversion
- `time`: high-precision timing for duration

#### constants:
- `MODEL_PATH`: path to Vosk model (downloaded manually, gitignored)
- `SAMPLE_RATE`: 16k samples/sec - hard model requirement, not changeable

#### module-level:
- `q = queue.Queue()`: shared between `callback` and `record_turn`
- if defined inside a function it resets each call, audio never reaches Vosk

#### callback(indata, frames, time, status):
- never called directly - sounddevice calls it automatically every 0.5 sec
- blocksize 8000 at 16000 samples/sec = 0.5 sec per chunk
- converts audio to bytes (sounddevice gives numpy array, Vosk needs bytes)

#### record_turn(current_speaker=None):
- `None` default: first call has no speaker yet, prompts for name
- subsequent calls skip prompt, recording starts immediately
- `full_text = ""`: starts empty, accumulates confirmed Vosk output during loop
- `AcceptWaveform`: returns True only

---

### common/helpers.py

Shared utilities used by main.py to load and save CSV files.
Keeps file I/O in one place - all stages use the same functions.

#### imports:
- `pandas`: read_csv and to_csv for CSV handling
- `os`: creates directories before saving

#### load_csv(filepath):
- reads CSV from disk into a Pandas dataframe
- Time O(n): reads n rows from disk
- Space O(n): stores n rows in memory

#### save_csv(df, filepath):
- `os.path.dirname`: extracts folder path from full filepath
- `os.makedirs`: creates folder if it doesn't exist
- `exist_ok=True`: no error if folder already exists
- `index=False`: suppresses Pandas row numbers from CSV output
- Time O(n): writes n rows to disk
- Space O(1): no new memory allocated, dataframe already exists

---

### enrichment/enrich_dataset.py

Takes corrected CSV as Pandas dataframe and adds five calculated columns.
No AI - pure Python calculation. Runs after correction is complete.
Time O(n) per operation, Space O(n) for new columns.

#### question_flag:
- `str(x)`: safety conversion - Pandas can read missing values as float NaN
- calling `.strip()` on NaN throws AttributeError, `str(x)` prevents this
- `.endswith("?")`: True if corrected text ends with question mark

#### num_words:
- `split()` with no argument handles multiple spaces between words
- `split(' ')` would count empty strings between double spaces

#### text_size_chars:
- `len(str(x))` counts everything: letters, spaces, punctuation
- Sergiu's version excluded spaces and punctuation - wrong answer

#### speech_rate_wps:
- `axis=1`: applies across each row, needs both `num_words` and `time_taken_sec`
- guard: if `time_taken_sec` is 0 returns 0 instead of `ZeroDivisionError`

#### speaker_turn_id:
- `groupby("name")`: groups all rows by speaker
- `cumcount()`: counts from 0 within each group
- `+1`: shifts to start at 1 as brief requires

---

### main.py

Entry point and orchestration layer for the full pipeline.
No logic - imports one function from each module.
Separation of concerns: each import represents one stage.

#### imports:
- one function per module, each representing one pipeline stage
- `datetime`: timestamps per turn
- `pandas`: converts list of dicts to dataframe after recording

#### file path constants:
- defined once at top, change in one place if needed
- three files protect each stage independently

#### correct_with_fallback(text):
- fallback chain: Gemini → Ollama → original text
- `except Exception as e`: catches error, stores as e, execution continues
- recording session cannot be killed by API failure

---

## Placeholder

### validation/__init__.py
-- walkthrough to be added after recording session and testing --

### analyse/__init__.py

- Takes the validated CSV and answers six questions about the meeting using pd.
- Final stage - reads from 'FINAL_FILE', prints results to console, nothing saved

#### imports:
- 'pandas': groupby, sum, mean, sort_values, for all calculations

#### analyse_dataset
- `pd.read_csv(filepath)`: Time O(n), Space: O(n) - same as `load_csv`

#### Q1 & Q2 - most/least words:
- `df.groupby("name")["num_words"].sum()`: one expensive groupby, reused for both questions
- `idmax()`/ `max()`: extracts the one speaker with the highest total and their count
- `idmin()` / `min`(): same pattern, lowest total
- single winner question → extract one val, no loop 

#### Q3 - total speaking time:
`df.["time_taken_sec"].sum():` no groupby b/c meeting-wide total [not per speaker]

#### Q4 - avg. speaking time per speaker
- 'df.groupby("name)["time_taken_sec"].mean()`: single speaker avg.
- `.items()` loop: "per speaker" questions need every value
- `idmax()` / `idmin()`: applies only to high/low qs , (not show all)

#### Q5 - most questions asked:
- `df[df["question_flag"] == True]`: filters to only rows w/ question
- same row structure, fewer rows - not new df shape
- `.groupby("name").size()`: counts filtered rows per speaker
- guard: `if not questions_per_speaker.empty` - if no qs the filter set is empty and `idmax()` would crash; prints clean message

#### Q6 - top 5 speakers by total speaking time:
- `df.groupby("name")["time_taken_sec"].sun()`: total time per speaker
- `sort_values(ascending=False)`: highest first
- `.head(5)`: takes top 5 [even though head default is 5, this makes the top 5 more explicit]
- `enumerate(top6.items()1)`: starts rank count at 1 instead of 0

#### Q7 avg. speech rate per speaker
- same patter as Q4: "per speaker" loops through all vals