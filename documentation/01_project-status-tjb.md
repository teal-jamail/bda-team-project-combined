# BDA Team Project — Status
## teal-jamail/bda-team-project-combined

## Meeting recap | (19.06)

### What happened
- Pipeline ran successfully end to end: 26 rows recorded, validation passed
- Video recording was attempted but postponed — Ebou was unable to join
- Alina sent final pre-submission task breakdown to the group
- Gemini rate limited at row 8/26 — 17 rows fell back to raw uncorrected text
  fix needed: 13-second delay between Gemini calls before final re-run
- question_flag all False on current data — raw Vosk text has no punctuation
  will resolve once Gemini delay fix is applied and correction re-runs

### Agreed
- Meet again tomorrow 10AM for final video recording
- If someone cannot attend, recording proceeds without them
- Monday 2PM is the submission deadline — tomorrow is the last opportunity

### Video sections agreed
- Teal: project overview and live demo
- Nita: architecture and AI correction pipeline  
- Sergiu: recording pipeline, integration, testing
- Alina: validation checks and error handling
- Ebou: dataset enrichment and README

### Post-recording tasks (before Monday 2PM)
- confirm GitHub repo complete and ready (everyone)
- generate final CSV with 25+ rows, clean re-run with Gemini delay fix (Teal)
- validation output saved (Alina)
- analytics output saved (Teal)
- README written and pushed (Ebou)
- upload all deliverables to OneDrive (Alina)
- share OneDrive with s.sotiriadis@bbk.ac.uk (Alina)
- individual peer evaluation forms submitted on Moodle (everyone)
- AI declaration on Moodle (everyone — not due Monday, flag for later)

~~## Thurs. discussion - quick reference~~
- - filename check: what main.py actually writes (correct_transcript.csv vscorrection_transcription.csv) - docs diff
- merge strategy agreed: Sergiu merging all branches into a separate integration branch first, main stays protected
- NOT blanket "accept theirs" - validation/__init__.py must come from main (tested, working) not Sergiu's or Alina's branch - both have a critical bug (validate() never returns True/False)
- main.py protected - last-turn fix already pushed to main, don't let it get reverted by Sergiu's incremental-write rewrite without comparison
- transcribe.py - wait for Nita's restructure push before reconciling
- Ebou has GitHub access now
- Alina's validation.py reviewed - has real bugs, see decision log~~

## In progress
- ~~analyse/__init__.py (Teal)~~
- ~~reviewing Sergiu's branch content (confirmed visible on GitHub: teal-jamail/bda-team-project-combined, branch Sergiu)~~
- ~~Nita actively implementing her transcribe.py/main.py restructure (not yet pushed)~~
- ~~validation/__init__.py - confirmed empty twice, rewritten a third time, verify push landed~~

---

## Not started
- !! recording session 
- requirements.txt update
~~- Vosk model download and local test (Sergiu)~~
- Review README for submission
- team video (Alina) — after pipeline complete

## Blockers
~~- pipeline cannot be fully tested until Vosk model downloaded locally and real recording data exists~~
~~- Sergiu's merge-all-branches plan needs the file-by-file exceptions communicated (sent to group) before he proceeds~~
~~- filename inconsistency flagged by Ebou: task_breakdown says correct_transcript.csv, merge log said correction_transcript.csv - confirm what main.py actually writes, fix whichever doc is wrong~~
~~- Ebou needs the three pipeline CSVs (raw_transcript.csv, correct_transcript.csv, final_transcript.csv) to run his data-quality checks - data/ is gitignored, not in repo~~
~~- decision needed: share files directly vs. temporarily committing real recorded data (leaning toward direct share)~~

20.06
## Blockers
- Gemini rate limiting: 17/26 rows fell back to raw text
  fix: add 13-second delay between calls before re-running correction
- question_flag all False because raw Vosk text has no punctuation
  will resolve once Gemini delay fix is applied
- README not yet written (Ebou)
- final 25-row CSV needs clean re-run with Gemini delay fix

---


~~## Next actions | (18.06)~~
- confirm Thursday recording session status with team
- discuss Nita's restructure once pushed
- verify CORRECT_FILE filename in main.py, fix whichever doc is wrong
- confirm validation/__init__.py push actually landed this time (verify via GitHub, not just local)
- get the three CSVs to Ebou once real data exists
- update requirements.txt
- write submission README
- review and incorporate complexity writeup into README (Ebou's is done, shared)
- record team video
- add validation walkthrough to 03_code-walkthrough-tjb.md (still placeholder)

~~## Next actions | (11.06)~~
- ~~write analyse/__init__.py~~
- update requirements.txt
- Vosk model download and local test (Sergiu)
- ~~Alina to write recording script~~
- ~~Mon 10:15 — group recording session (pipeline data, not video)~~
- ~~complexity writeup (Ebou)~~
- write submission README
- record team video (after pipeline complete)
- upload video to OneDrive → share with s.sotiriadis@bbk.ac.uk
- add validation walkthrough to code-walkthrough-tjb.md once written
- ~~Nita & Serg to review documentation~~

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
  - analyse/__init__.py

- bugs found and fixed from Sergiu's codebase (Teal):
  - full_text bug in transcribe.py
  - count_characters counted letters only
  - speach_rate_wps typo
  - final_result.duration vs time_taken naming clash
  - wrong CSV column names throughout
  - missing time_taken_sec and speech_rate_wps from CSV
  - fixed loop producing only 5 rows

- last-turn data loss bug found independently in our own main.py (same bug Sergiu found on his branch) - fixed and pushed to main

- architecture decisions made and documented (Teal):
  - Pandas enrich_dataframe over process_raw_text.py
  - zero-guard added to speech_rate_wps division
  - column names standardised to match brief exactly
  - correct_with_fallback as correction strategy
  
- documentation/ folder created (Teal):
  - 01_project-status-tjb.md
  - 02_merge_decision_log-tjb.md
  - 03_code-walkthrough-tjb.md
  - 04_task_breakdown-tjb.md
  - notes-ntm.txt
- first push to GitHub complete

- annotated code docs preserved in documentation/annotated_code_docs/
- team-notes-overview-tjb.md deleted (content distributed across other docs)
- task_breakdown-tjb.md written and sent to team (11.06)
- 11.06 meeting rundown sent via email and group chat

- analyse/__init__.py written, tested against synthetic data, walkthrough added
- Sergiu (diasergiu), Nita (itsNTM) and Ebou (Njies08) added as GitHub collaborators
- Alina submitted her validation.py - reviewed against Sergiu's integration attempt, found critical bugs (missing return value, disabled row-count check, wrong CSV separator) - documented in 02_merge_decision_log-tjb.md, not merged
- Ebou's enrichment work fully complete: enrich_dataset.py finished, complexity writeup shared with the team
- merge strategy agreed: Sergiu integrating all branches on a separate branch,
  file-by-file review rather than blanket accept (replied with specifics on
  validation/__init__.py, main.py, transcribe.py)


20.06
- pipeline ran successfully: 26 rows recorded, validation passed
- video recording attempt made but postponed (Ebou absent)
- Alina sent final pre-submission task breakdown to group