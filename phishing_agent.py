# ADVANCED PHISHING DETECTION SCRIPT – CONFIGURABLE MODES
# Supports basic BERT analysis and optional advanced header/domain checks

import os
import mailparser
import extract_msg
from transformers import pipeline, AutoTokenizer
import requests

# === CONFIGURATION FLAGS ===
USE_ADVANCED_ANALYSIS = False  # Set to False for basic BERT-only mode
API_KEY_APIVOID = os.getenv("APIVOID_API_KEY", "")  # Set via environment variable

# === INPUT FILE ===
email_path = "examples/sample-2.msg"  # or .msg
ext = os.path.splitext(email_path)[1].lower()

# === PARSING EMAIL ===
if ext == ".eml":
    parsed = mailparser.parse_from_file(email_path)
    subject = parsed.subject
    body = parsed.body
    headers = parsed.headers
    sender = parsed.from_[0][1] if parsed.from_ else ""
    reply_to = parsed.reply_to[0][1] if parsed.reply_to else ""
    return_path = parsed.return_path[0] if parsed.return_path else ""
elif ext == ".msg":
    msg = extract_msg.Message(email_path)
    subject = msg.subject
    body = msg.body
    headers = {}
    sender = msg.sender or ""
    reply_to = ""
    return_path = ""
else:
    raise ValueError("Unsupported file type. Use .eml or .msg")

print("--- SUBJECT ---\n", subject)
print("\n--- BODY ---\n", body)
print("\n--- SENDER ---\n", sender)
print("--- RETURN PATH ---\n", return_path)

# === BERT CLASSIFICATION ===
classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")

inputs = tokenizer(body, truncation=True, max_length=512)
decoded_input = tokenizer.decode(inputs["input_ids"], skip_special_tokens=True)
result = classifier(decoded_input)
ai_score = result[0]['score'] if result[0]['label'] == 'LABEL_1' else 1 - result[0]['score']

# === ADVANCED ANALYSIS FUNCTIONS ===
def extract_domain(email):
    return email.split("@")[-1].lower() if "@" in email else ""

def check_domain_reputation(domain):
    if not API_KEY_APIVOID:
        print("⚠️ No API key for APIVoid. Skipping domain reputation check.")
        return 0.0
    try:
        url = f"https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key={API_KEY_APIVOID}&host={domain}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            detections = data.get("data", {}).get("report", {}).get("blacklists", {}).get("detections", 0)
            return min(detections / 5, 1.0)  # Normalize score (max 1.0)
        else:
            return 0.0
    except Exception as e:
        print(f"Error checking domain reputation: {e}")
        return 0.0

# === HEADER ANALYSIS (IF ENABLED) ===
header_score = 0.0
if USE_ADVANCED_ANALYSIS:
    sender_domain = extract_domain(sender)
    return_domain = extract_domain(return_path)

    if sender_domain and return_domain and sender_domain != return_domain:
        header_score += 0.5

    domain_reputation_score = check_domain_reputation(sender_domain)
    header_score += domain_reputation_score
    header_score = min(header_score, 1.0)

# === FINAL PHISHING SCORE ===
final_score = round(0.6 * ai_score + 0.4 * header_score, 2) if USE_ADVANCED_ANALYSIS else round(ai_score, 2)
label = "Phishing" if final_score >= 0.65 else "Legitimate"

print(f"\nFinal phishing score: {final_score} → {label}")

# === OUTPUT TO FILE ===
with open("analysis_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Subject: {subject}\n")
    f.write(f"Sender: {sender}\n")
    f.write(f"Return-Path: {return_path}\n")
    f.write(f"AI Score: {ai_score:.2f}\n")
    if USE_ADVANCED_ANALYSIS:
        f.write(f"Header Score: {header_score:.2f}\n")
    f.write(f"Final Score: {final_score} → {label}\n")