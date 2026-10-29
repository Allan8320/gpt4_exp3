
from utils import ask_ollama


def improve_tone(reply, tone):
    prompt = f"""
Rewrite the following customer support email in a {tone} tone.

Preserve the original meaning and all factual details.
Do not invent promises, approvals, or actions.
Return only the rewritten email.

Email:
{reply}
"""

    return ask_ollama(prompt)
