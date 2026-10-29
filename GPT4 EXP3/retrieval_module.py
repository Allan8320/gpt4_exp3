
import csv
import re
from pathlib import Path


def tokenize(text):
    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def find_similar_email(customer_email, csv_path):
    path = Path(csv_path)

    if not path.exists():
        return None

    current_words = tokenize(customer_email)
    if not current_words:
        return None

    best_row = None
    best_score = 0

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            previous_email = row.get("Email", "")
            previous_reply = row.get("Reply", "")

            old_words = tokenize(previous_email)
            union = current_words | old_words

            if not union:
                continue

            score = len(current_words & old_words) / len(union)

            if score > best_score:
                best_score = score
                best_row = {
                    "email": previous_email,
                    "reply": previous_reply
                }

    return best_row
