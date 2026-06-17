# BDA Team Project — Status
## teal-jamail/bda-team-project-combined

## Thrs. discussion - quick reference
- filename check: what main.py actually writes (correct_transcript.csv vscorrection_transcription.csv) - docs diff
- Serg's branch: incremental CSV writes + last-tune fix - review before merge
- Nita's restructure: move speaker input from transcribe.py into main.py
- Teal found same last-turn bug in the main.py - needs fix either way
- Ebou has github access
- Alina has validation file


## In progress
- ~~analyse/__init__.py (Teal)~~
- reviewing Sergiu's and Nita's local branch changes (not yet pushed to GitHub) last check - git fetch showed only main
- locating and comparing Alina's validation submission against current validation/__init__.py

---

## Not started
- !! recording session
- requirements.txt update
- Vosk model download and local test (Sergiu)
- ~~Alina recording script~~
- ~~README for submission~~
- ~~complexity writeup (Ebou)~~
- team video (Alina) — after pipeline complete

## Blockers
- pipeline cannot be tested until Vosk model downloaded locally and have REAL data from recording session 
- Serg and Nita branchs not yet visible - need push for team review
- filename inconsistency flagged by Ebout: task_breakdown says correct_transcription.csv, merge log said correction_trascript.csv - confirm main.py writes and fix docs
- Ebou needs the three pipeline CSVs (raw_transcript.csv, correct_transcript.csv, final_transcript.csv) to run his data-quality checks - data/ is gitignored - not yet in repo 

Decision needed: share files directly vs. temporarily committing real recorded data (leaning toward direct share, not committing real speech data to git history)

---

## Next Actions | (06.15)
- confirm thursday full recording and run
- discuss Nit'a restrure
- verify CORRECT_FILE filename in main.py, fix
- locate and compare Alina's validation ( update logs and annote)
- locate and compare Ebous enrichment ( update logs and annotate)
- Ebou three CSVs for check?
- fix last-turn bug in main.py (`all_data.append()` before `input()` prompt)
- update requirements txt
- write/update/ merge README
- review complexity writeup
- record tema vids

## Next actions | (11.06)
- ~~write analyse/__init__.py~~
- update requirements.txt
- Vosk model download and local test (Sergiu)
- ~~Alina to write recording script~~
- ~~Mon 10:15 — group recording session (pipeline data, not video)~~
- ~~complexity writeup (Ebou)~~
- write submission README
- record team video (after pipeline complete)
- upload video to OneDrive → share with s.sotiriadis@bbk.ac.uk
- add validation ~~and analyse~~ walkthroughs to code-walkthrough-tjb.md once written
- ~~Nita & Serg to review documention~~

## Next actions | (08.06)
- ~~copy for annoted and save originals .py~~
- ~~write analyse/__init__.py~~
- update requirements.txt
- ~~schedule recording session~~

---

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

- annotated code docs preserved in documentation/annotated_code_docs/
- team-notes-overview-tjb.md deleted (content distributed across other docs)
- task_breakdown-tjb.md written and sent to team (11.06)
- 11.06 meeting rundown sent via email and group chat

- analyse/__init__.py written, tested against synthetic data, walkthrough added
- Sergiu (diasergiu), Nita (itsNTM) and Ebou added as GitHub collaborators -  
- Alina completed and submitted her validation work in group chat (referenced Nita's script plus her own additions; Nita reviewed it live and confirmed it looks good)
- Ebou's enrichment work fully complete: enrich_dataset.py finishe complexity writeup shared with the team
