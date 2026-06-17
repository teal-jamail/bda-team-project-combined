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

MODEL_NAME = "gemma3"
OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(prompt):
    prompt.append("\n\n Correct the transcript above. Return only the corrected sentence, without any additional text or explanation.")
    # this sends a POST request to the Ollama server and asks the Ai model to correct the transcript.
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()

    return response.json()["response"].strip()



if __name__ == "__main__":
    prompt = (
        "Correct this transcript. Return only the corrected sentence:\n"
        "can we target students first"
    )

    output = ask_ollama(prompt)
    print(output)