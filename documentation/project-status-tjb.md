# BDA Team Project — Status
## teal-jamail/bda-team-project-combined

## Done
- repo created and maintained: teal-jamail/bda-team-project-combined
- folder structure designed by Nita; added Teal's documentation 
- both codebases reviewed, assessed, and merged by Teal (diasergiu, itsNTM)
- all files annotated (Teal):
  - vosk_transcription/transcribe.py
  - ai_correction/gemini_correct.py
  - ai_correction/ollama_correct.py
  - enrichment/enrich_dataset.py
  - common/helpers.py
  - main.py
  - validation/__init__.py
  - analyse/__init__.py (placeholder)

- bugs found and fixed from Sergiu's codebase (Teal):
  - full_text bug in transcribe.py
  - count_characters counted letters only
  - speach_rate_wps typo
  - final_result.duration vs time_taken naming clash
  - wrong CSV column names throughout
  - missing time_taken_sec and speech_rate_wps from CSV
  - fixed loop producing only 5 rows

- architecture decisions made and documented (teal):
  - Pandas enrich_dataframe over process_raw_text.py
  - zero-guard added to speech_rate_wps division
  - column names standardised to match brief exactly
  - correct_with_fallback as correction strategy
  
- documentation/ folder created (Teal):
  - team-notes-overview-tjb.md
  - code-walkthrough-tjb.md
  - project-status-tjb.md
  - notes-ntm.txt
- first push to GitHub complete

## In progress
- analyse/__init__.py (Teal)

## Not started
- !! recording session (all 5 people, 25 rows minimum)
- requirements.txt update
- Vosk model download and local test
- README for submission
- complexity writeup (Ebou)
- team video (Alina)

## Blockers
- pipeline cannot be tested until Vosk model downloaded locally
- recording session needs all 5 people present

## Next actions
- write team instructions
- write analyse/__init__.py
- update requirements.txt
- schedule recording session
