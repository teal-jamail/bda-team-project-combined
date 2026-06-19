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
from common.prompts import CORRECTION_PROMPT

MODEL_NAME = "gemma3"
OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(text):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME, 
                "prompt": CORRECTION_PROMPT.format(text=text),
                "stream": False
            },
            timeout=120,
        )

        response.raise_for_status()
        
        return response.json()["response"].strip()
    
    except Exception as e:
        print("Ollama failed:", e)
        return None

