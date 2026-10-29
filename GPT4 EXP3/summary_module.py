
from utils import ask_ollama


def summarize_email(email):
    prompt = f"""
Summarize the customer's issue in exactly 50 words.
Mention the main problem and any requested action.
Do not invent details.

Customer email:
{email}

Return only the summary.
"""

    return ask_ollama(prompt)
