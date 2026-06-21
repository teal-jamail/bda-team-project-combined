CORRECTION_PROMPT = """
Correct this transcript.

Task: Fix grammar, spelling, and punctuation.
Rules:
- Return only the corrected sentence
- Add proper full stops and capitalization
- Do not add explanation
- Do NOT convert questions into statements
Input: {text}
"""