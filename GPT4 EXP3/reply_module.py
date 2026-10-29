
from utils import ask_ollama


def generate_reply(name, subject, email, previous_reply=None):
    reference = previous_reply or "No similar previous reply was found."

    prompt = f"""
You are a professional customer support email assistant.

Customer name: {name}
Subject: {subject}
Customer email:
{email}

Similar previous reply for reference:
{reference}

Write a concise, polite and relevant email reply.
Use the reference only when helpful.
Do not invent order status, refund approvals, delivery dates,
or actions that have not been confirmed.
Do not include explanations about how you generated the reply.
Return only the email reply.
"""

    return ask_ollama(prompt)
