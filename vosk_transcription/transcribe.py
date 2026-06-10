"""Simple Vosk example.

This records from the microphone, transcribes speech with Vosk, prints the
transcript, and saves it to transcript.txt.
"""

import json
# vosk returns results JSON ['json.loads()']
# converts those strs into py dicts to pull txt

import queue
# thread-safe queu; mic runs in 1 thread, vosk another
# processes run together
# passes audio chunks b/t w/o mixing data

from datetime import datetime

import sounddevice as sd
# captures raw audion from mic as stream

from vosk import Model, KaldiRecognizer
# Model loads speech recognition from disk
# kaldiRecognizer handles speech-to-text conversion

import time 
# high-precision timing for duration


MODEL_PATH = "vosk-model-en-us-0.22-lgraph"
# define model w/ reusable df
SAMPLE_RATE = 16000
# 16k audio samples per sec - expects audio as exact frequency
OUTPUT_FILE = "transcript.txt"

q = queue.Queue()
# defined at model level 
# callback & record share same queu instance

def callback(indata, frames, time, status):
    # auto-called by 'sounddevice' w/ ea. new chunck of audio from mic
    # pass sd.RawInputStream & 
    # sd continually calls in background while mic is open
    if status:
        print(status)
    q.put(bytes(indata))
    # converts audion data into raw bytes format
    # what vosk 'AcceptWaveform' mehtod expects
    # SD gives audio as np arr & vosk needs raw bytes
    # bridges two libraries


model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

def record_turn(current_speaker=None):
    if current_speaker is None:
        current_speaker = input("Enter speaker name: ").strip()
    print(f"\n[{current_speaker}] Start speaking. Press Ctrl+C when done.")
    start_time = time.perf_counter()
    full_text = ""
    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        print("Heard:", text)
                        full_text += text + " "
    except KeyboardInterrupt:
        print("\nStopped recording.")
    end_time = time.perf_counter()
    final_result = json.loads(recognizer.FinalResult())
    final_raw_text = final_result.get("text", "")
    duration = round(end_time - start_time, 2)
    phrase = (full_text + final_raw_text).strip()
    return current_speaker, phrase, duration
