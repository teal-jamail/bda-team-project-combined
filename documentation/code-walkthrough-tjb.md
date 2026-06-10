# BDA Team Project — Code Walkthrough

### ai_correction/ollama_correct.py

* sends raw vosk txt to local ollama server for correction
* ollama runs locally (http://localhost:11434) - no internet needed

imports:
- requests: sends Http request to local ollama server

constants at top (defined once for reuse):
- MODEL_NAME: uses gemma3
- OLLAMA_URL: address local ollama API endpoint

ask_ollama(prompt):
- posts prompt to ollama w/ stream:False (returns full respons, not token-by-token)
- raise_for_status(): error handling - stops if server returns error code
- returns corrected txt stripped of extra ws

if __name__ == "__main__":
- test block - runs only when file directly executed
- doesn't run when main.py imports ask_ollama
- can test ollama works w/o running full pipeline

---

### ai_correction/gemini_correct.py

- sends raw vosk txt to gemini api to correct
- requires GEMINI_API_KEY exported as environmental var

imports:
- os: reads GEMINI_API_KEY from environment (so not in db)
- google.genai: Gemini API client library

contatnts at top:
- MODEL_NAME: which gemini model to use (gemini-2.5-flash)

ask_gemini(text):
- creates client using API key from environment
- build prompt: correct transcript, return only corrected sentence
- generates respons using model & prompt
- returns correct txt w/o trailing new lines

differs from ask_ollama:
- no local server - sends requests to googles API vis net
- raises KeyError if key missing or invalid

---

### vosk_transcription/transcribe.py

- Records one speaker turn via mic & returns transcript duration
- uses vosk for offline speech-to-text - no web needed

imports:
- json: vosk returns results as JSON strings, json.loads() converts to dict
- queue: thread-safe queues, mic runs in one thread, vosk process in other
- sounddevice: capture raw audio from mic as stream
- vosk Model: loads speech recognition model from disk
- vosk KaldiRecognizer: speech-to-text conversion
- time: high-precision timing for duration measurement

constants:
- MODEL_PATH: path to vosk model (must dnlwd manual; gitignored)
- SAMPLE_RATE: 16k samples/sec - hard model requirement; can't change

module-level:
- q = queu.Queu(): shared b/t callback and record_rurn
- if call 'q' inside function it resets ea. call & audio doesnt reach vosk

callback(indata, frames, time, status):
- nvr called directly - sd auto-calls every 1/2 sec
- blocksize 800 at 16k smple/sec - .5 sec. per chunck
- converts audio to bytes (sd gives np arr, vosk needs bytes)

record_turn(current_speaker=None)
- default = None: 1st call has no speaker, prompts for name
- subsequent calls skip prompt & start recording immediately
- full_text = "": initialised empty, accumulates confirmed vosk output during loop
- AcceptWaveForm returns true only when vosk has complete & recognizable phrase
- result.get("text", ""): safe dict access, return empty str if key missing
- if text: guard against silence/noise - accumulates real content only
- end_time outside except: capture time whether recording stopped or not
- final_raw_text: last fragment that was processing when ctrl+c pressed
- phrase = (full_text + final_raw_text).strip(): combines both for complete utterance
- Sergiu's bug: returned only final_raw_text, discarding full_text
- returns: speaker name, full phrase, duration in sec.

---

## common/helpers.py

- Shared utilities used by main.py to load and save csv file
- Keeps file i/o in one place - all stages use same functions

imports:
- pandas: read_csv and to_csv for handling
- os: creates directories b4 saving

load_csv(filepath):
- read csv from disk to pd df
- Time: O(n): reads 'n' rows from disk
- Space: O(n): stores rown in memory

save_csv(df, filepath):
- os.path.dirname extracts folder path from full filepath
- os.maksdirs creates folder itself if doesn't exist
- exist_ok=True: no error if folder already exists
- index=false: turn of pd's rom nums from csv putput
- Time: O(n): write n rows to disk
- Space: O(1): no new memory, df already there

---

## enrihment/enrich_dataset.py

- Takes the correct csv as a pd df and adds five calculated cols.
- No AI - only python calc. Runs post-correction
- Time: O(n) per operation, Space: O(n) for new col.

question_flag:
- str(x): safety conversion - pd can read null vals as flt NaN
- calling .strip() on NaN gives AttributeError, str(x) prevents this
- .endswith("?"): True if corrected text ends w/ quesiton mark

num_words:
- split() with no argument handles multiple spaces b/t words
- split(' ') would count emplty str b/t double spaces

text_size_chars:
- len(str(x)) inclusive of letters, spaces, punctuation
- Sergiu's version excluded spaces and punctuation

speech_rate_wps:
- axis=1, applies acrosse ea. row, needs both num_words & time_taken_sec
- guard: if time_taken_sec is 0 it returns 0 instead of ZeroDivisionError

speaker_turn_id:
- group.by("name"): groups all rows by speaker
- cumcount(): default counts python from 0 w/in ea. group
- +1: starts count at 1 instead of 0

## main.py

- Entry & orchestration layer for full pipeline
- no logic

imports:
- imports one func. from ea. module
- seperates concerns: ea. import represents one stage

file path constants:
- defined once at top, change in one place if need
- three files protect ea. stage independantly
    -   RAW_FILE: safe if stages 2/3 crash
    -   CORRECT_FILE: safe if stage 3 crashes
    -   FINAL_FILE: read by validation and analytics

correct_with_fallback(text):
- fallback chain: gemini -> Ollama -> orgin. txt
- except Exception as e: catches error, stores as e, continues
- recording session cannot be killed by API failure

