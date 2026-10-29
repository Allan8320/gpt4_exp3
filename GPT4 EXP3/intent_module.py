
from utils import ask_ollama

ALLOWED_INTENTS = [
    "Delivery Issue",
    "Refund Request",
    "Product Complaint",
    "Technical Support",
    "Order Cancellation",
    "General Inquiry"
]


def detect_intent(customer_email):
    prompt = f"""
Classify the customer email into exactly one category:
{", ".join(ALLOWED_INTENTS)}

Customer email:
{customer_email}

Return only the category name. Do not explain.
"""

    result = ask_ollama(prompt)

    for intent in ALLOWED_INTENTS:
        if result.lower().strip().startswith(intent.lower()):
            return intent

    return "General Inquiry"
