
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pathlib import Path
import csv
import requests

from intent_module import detect_intent
from retrieval_module import find_similar_email
from reply_module import generate_reply
from tone_module import improve_tone
from summary_module import summarize_email

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "emails.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "generated_reply.txt"


def get_ollama_status():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.ok
    except requests.RequestException:
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}

    name = data.get("customer_name", "").strip()
    subject = data.get("subject", "").strip()
    email = data.get("email", "").strip()

    if not name or not subject or not email:
        return jsonify({"error": "Please complete all email fields."}), 400

    try:
        intent = detect_intent(email)
        previous = find_similar_email(email, DATA_FILE)
        previous_reply = previous.get("Reply", "") if previous else ""

        reply = generate_reply(name, subject, email, previous_reply)
        summary = summarize_email(email)

        return jsonify({
            "intent": intent,
            "previous_email": previous.get("Email", "") if previous else "",
            "previous_reply": previous_reply,
            "reply": reply,
            "summary": summary
        })
    except Exception as error:
        app.logger.exception("Email analysis failed")
        return jsonify({"error": str(error)}), 500


@app.route("/api/tone", methods=["POST"])
def tone():
    data = request.get_json(silent=True) or {}
    reply = data.get("reply", "").strip()
    selected_tone = data.get("tone", "Professional")

    if not reply:
        return jsonify({"error": "Generate a reply first."}), 400

    try:
        improved = improve_tone(reply, selected_tone)
        return jsonify({"reply": improved})
    except Exception as error:
        app.logger.exception("Tone improvement failed")
        return jsonify({"error": str(error)}), 500


@app.route("/api/save", methods=["POST"])
def save():
    data = request.get_json(silent=True) or {}

    required = ["customer_name", "subject", "email", "intent", "reply"]
    if any(not str(data.get(field, "")).strip() for field in required):
        return jsonify({"error": "Missing email or reply details."}), 400

    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open("a", encoding="utf-8") as file:
            file.write("\n" + "=" * 55 + "\n")
            file.write("Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            file.write("Customer: " + data["customer_name"] + "\n")
            file.write("Subject: " + data["subject"] + "\n")
            file.write("Customer Email: " + data["email"] + "\n")
            file.write("Intent: " + data["intent"] + "\n")
            file.write("Reply: " + data["reply"] + "\n")
            file.write("Summary: " + data.get("summary", "") + "\n")

        return jsonify({"message": "Reply saved to outputs/generated_reply.txt"})
    except OSError as error:
        app.logger.exception("Saving reply failed")
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    print("MailMind AI starting...")
    print("Ollama available:", get_ollama_status())
    app.run(debug=True, port=5000)
