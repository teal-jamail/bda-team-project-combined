# Speech Analytics Pipeline — BDA Team Project
A speech-to-analytics pipeline that records spoken meeting dialogue, transcribes it, corrects the transcription with an LLM, enriches it with calculated features, validates the output, and produces analytics on speaker behaviour.

## What it does
The pipeline turns a recorded multi-speaker conversation into a structured, analysed dataset. Each speaker turn is captured, transcribed offline with Vosk, cleaned up by an AI correction step, enriched with per-turn metrics (word counts, speech rate, question detection, speaker turn numbering), checked for data-quality issues, and finally analysed.

## Pipeline stages
The pipeline runs in five stages, orchestrated by main.py:

**Stage 1 — Transcription (vosk_transcription/transcribe.py)**
Captures microphone audio per speaker turn using `sounddevice`, converts speech to text offline with the Vosk model (KaldiRecognizer), and records the timestamp, speaker name, raw Vosk text, and time taken per utterance. Output is saved to `data/raw_transcript.csv`.

**Stage 2 — AI correction (ai_correction/)**
Takes the raw Vosk text and sends it to an LLM for grammar and punctuation correction — Gemini first, falling back to Ollama, and keeping the original text if both fail (`correct_with_fallback`). The corrected text is stored in a new `text` column. Output is saved to `data/correct_transcript.csv`.

**Stage 3 — Enrichment (enrichment/enrich_dataset.py)**
Adds five calculated columns to the corrected transcript using pandas (no AI). See the Enrichment Complexity section below for details. Output is saved to `data/final_transcript.csv`.

**Stage 4 — Validation (validation/)**
Checks the final dataset for errors and data-quality issues. If validation fails, the pipeline stops and reports the issues to fix.

**Stage 5 — Analysis (analyse/)**
Runs analytics on the validated dataset — for example, who spoke the most and who asked the most questions.

## Project structure
bda-team-project-combined/

├── main.py                      # orchestrates the full pipeline

├── vosk_transcription/          # Stage 1: audio capture + speech-to-text

├── ai_correction/               # Stage 2: LLM correction (Gemini / Ollama)

├── enrichment/                  # Stage 3: feature engineering

│   └── enrich_dataset.py

├── validation/                  # Stage 4: data-quality checks

├── analyse/                     # Stage 5: analytics

├── common/                      # shared helpers

├── data/                        # pipeline output CSVs

│   ├── raw_transcript.csv

│   ├── correct_transcript.csv

│   └── final_transcript.csv

└── documentation/               # project docs

## How to run

1. Install dependencies:
pip install -r requirements.txt
2. Download the Vosk model and place it where `transcribe.py` expects it.
3. Run the full pipeline:
python main.py
4. Follow the prompts to enter each speaker's name and record their turn. The pipeline then runs correction, enrichment, validation, and analysis, writing the three CSVs to `data/`.

## Output files
- data/raw_transcript.csv — timestamp, name, raw_text_vosk, time_taken_sec
- data/correct_transcript.csv — the above plus a corrected `text` column
- data/final_transcript.csv — the above plus the five enrichment columns

---
## Enrichment Complexity
enrich_dataframe (in enrichment/enrich_dataset.py) adds five calculated columns to the corrected dataframe. In every case **n = the number of rows in the dataset** (one row per recorded speaker turn). No AI is used here — it is pure Python / pandas calculation.

**1. question_flag — O(n) time, O(n) space.**
Uses .apply() to visit each of the n rows once and check whether its `text` ends with `?`. One constant-time string check per row → n × O(1) = O(n). Stores one boolean per row → O(n) space.

**2. num_words` — O(n) time, O(n) space.**
.apply() visits each of the n rows once and splits text on whitespace to count words. (Splitting a single row's string is proportional to that string's length, but sentence length is bounded and small, so it is treated as constant per row.) n rows × O(1) = O(n). One integer per row → O(n) space.

**3. text_size_chars — O(n) time, O(n) space.**
.apply() visits each of the n rows once and calls `len()` on the string. One length read per row → O(n). One integer per row → O(n) space.

**4. speech_rate_wps — O(n) time, O(n) space.**
df.apply(..., axis=1)` visits each of the n rows once, dividing num_words by time_taken_sec. A zero-guard returns 0 instead of dividing when time_taken_sec is 0, preventing a division-by-zero crash on bad data. One arithmetic operation per row → O(n). One float per row → O(n) space.

**5. speaker_turn_id — O(n) time, O(n) space.**
df.groupby("name").cumcount() + 1 scans all n rows to assign each speaker a running turn count (their 1st, 2nd, 3rd turn…). The grouping uses hash-based bucketing, which is O(n) on average, and the running count then passes over every row once → O(n). One integer per row → O(n) space.

**Overall:** five sequential O(n) passes → **O(n) time**. Total added storage is five new columns of n values → **O(n) space**. The enrichment stage scales linearly with the number of recorded turns.
