"""Simple Gemini example.

Enter a prompt, send it to Gemini, and print the output.

Set GEMINI_API_KEY before running:
    export GEMINI_API_KEY="your_key_here"
"""

import os
from google import genai
from common.prompts import CORRECTION_PROMPT

MODEL_NAME = "gemini-2.5-flash" 


def ask_gemini(text):
    try:
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        
        prompt = CORRECTION_PROMPT.format(text=text)

        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)

        return response.text.strip()
        
    except Exception as e:
        print("Gemini failed:", e)
        return None

