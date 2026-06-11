"""Simple Ollama example.

Enter a prompt, send it to a local Ollama model, and print the output.

Before running:
    1. Install Ollama from https://ollama.com/download
    2. Open the Ollama app, or make sure the local Ollama server is running
       at http://localhost:11434
    3. Download the model:
       ollama pull gemma3
"""

import requests
# library for sending http request to server

MODEL_NAME = "gemma3"
OLLAMA_URL = "http://localhost:11434/api/generate"
# df to call once

def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        # retrieve gemma via df MODEL_NAME, pull prompt from ask_ollama
        # stream: False waits until full correction to return (vs. stream response tokens)
        timeout=120,
    )
    response.raise_for_status()
    # error handling: raises exception, 
    # stops code so dont get broken response

    return response.json()["response"].strip()
    # response.json() converts server's response from raw text to pythong dict
    # '["response"]' pulls correct txt from dictionary
    # '.strip()' removes extra ws or new lines from edges


if __name__ == "__main__":
    prompt = (
        "Correct this transcript. Return only the corrected sentence:\n"
        "can we target students first"
    )
    # creats text correction prompt and 
    # returns only corrected txt on new line
    # inputs raw text for correction

    output = ask_ollama(prompt)
    print(output)

    # 'main.py' from 'ai_correction.ollama_correct' imports ask_ollama
    # test block to run file seperately and check ollama works
    # no pipeline interference
