"""Simple Gemini example.

Enter a prompt, send it to Gemini, and print the output.

Set GEMINI_API_KEY before running:
    export GEMINI_API_KEY="your_key_here"
"""

import os

from google import genai


MODEL_NAME = "gemini-2.5-flash" 
# reusable df to call gemini


def ask_gemini_to_correct(text_to_correct):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    # create client using key
    
    prompt = (
        "Correct this transcript. Return only the corrected sentence:\n"
        f"{text_to_correct}"
        # prompts to correct sentences from .csv
    ) # question to send to gemini

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    #generate content, call model and get content of the 'prompt
    return response.text.strip()
    # added .strip to remove tailing new lines

