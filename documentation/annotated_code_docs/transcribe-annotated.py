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
    # 1st call crrent speaker is None b/c no one has spoken
    if current_speaker is None:
        current_speaker = input("Enter speaker name: ").strip()
    # prompts user to enter speaker name, then strips ws
    # None is signal to ask for name 
    # subsequent calls current_speaker has name - skips if block
    # recording starts

    print(f"\n[{current_speaker}] Start speaking. Press Ctrl+C when done.")

    start_time = time.perf_counter()
    # exact moment recording starts - duration later

    full_text = ""
    # initialize an empty str
    # accumulates everything vosk hears during turn
    # starts empty [ "" ] gets added to 

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            # 8k sammples at 16k samples per sec
            # .5 sec. of audio per chunk
            dtype="int16",
            # ea. audio sample stored as 16-bit int
            channels=1,
            # one stream audio
            # mono audio for vosk [stereo would be 2]
            callback=callback,
            # ea. time fires gets .5 sec audio and adds to queu
        ):
            while True:
                data = q.get()
                # blocks and waits for available audio - then pulls
                # recording chunck puts thread in and processing thread pulls one at a time
                if recognizer.AcceptWaveform(data):
                    # returns True when vosk has enough audio to produce complete recogniable phrase
                    # if only runs when vosk has something to add - not per audio chunk
                    
                    result = json.loads(recognizer.Result())
                    # stores as json after load into recogizer
                    text = result.get("text", "")
                    # dict method - if 'text' key doesnt exist, returns empty str
                    
                    if text:
                        # guard against noice; 
                        print("Heard:", text)
                        full_text += text + " "
                        # only accumulate and print when actual content
                        # no empty str padding 'full_text'

    except KeyboardInterrupt:
        print("\nStopped recording.")

    end_time = time.perf_counter()
    # outside except: 
    # captures time whether rcording stopped or any other way

    final_result = json.loads(recognizer.FinalResult())
    # load final result from recognizer as json into final_result

    final_raw_text = final_result.get("text", "")
    # get text or "" from final result and store raw text 

    duration = round(end_time - start_time, 2)
    # calc. duration end - start time w/ 2 decimal places

    phrase = (full_text + final_raw_text).strip()
    # full_text accumulates everything from vosk during loop via AcceptWaveForm
    # when stop talking (ctrl+C) 
    # often there's half-a sentence or so that hasnt been recorded
    # final_raw_text: fragments vosk was still process when stopped
    # if keep only full text:lose everything confirmed in session
    # if only full_text: keep only the fragment
    # combining both: complete w/ nothing cut off at the end
    # Sergiu's bug: returned only final_raw_text, discarding full_text

    return current_speaker, phrase, duration
    # return speaker name, 
    # what they said and 
    # how long it took to say
