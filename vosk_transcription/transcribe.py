"""Simple Vosk example.

This records from the microphone, transcribes speech with Vosk, prints the
transcript, and saves it to transcript.txt.
"""

import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import time 


MODEL_PATH = "vosk-model-en-us-0.22-lgraph"
SAMPLE_RATE = 16000

q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)


def record_turn(current_speaker):
    # 1st call crrent speaker is None b/c no one has spoken
    # if current_speaker is None:
    #     current_speaker = input("Enter speaker name: ").strip()

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

    # return current_speaker, phrase, duration
    return phrase, duration
