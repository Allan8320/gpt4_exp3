
import requests


def detect_intent(customer_email):
    prompt = f"""
You are a customer support email classifier.

Classify the email into exactly ONE of these categories:
Delivery Issue
Refund Request
Product Complaint
Technical Support
Order Cancellation
General Inquiry

Customer email:
{customer_email}

Return only the category name. Do not explain.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()["response"].strip()

        allowed_intents = [
            "Delivery Issue",
            "Refund Request",
            "Product Complaint",
            "Technical Support",
            "Order Cancellation",
            "General Inquiry"
        ]

        for intent in allowed_intents:
            if intent.lower() in result.lower():
                return intent

        return "General Inquiry"

    except requests.exceptions.RequestException as error:
        print("Intent detection error:", error)
        return "General Inquiry"
