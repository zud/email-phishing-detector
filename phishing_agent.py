# phishing_agent.py – CLI Phishing Analyzer v1.4.0 Final (Fully Silenced + Advanced Logic)

import os
import re
import sys
import io
import traceback
import contextlib
import yaml
import requests
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
from email import policy
from email.parser import BytesParser
import extract_msg
from fuzzywuzzy import fuzz

# === Force UTF-8 for console ===
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === Suppress stdout and stderr completely ===
@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, 'w') as fnull:
        fd_stdout = sys.stdout.fileno()
        fd_stderr = sys.stderr.fileno()
        saved_stdout = os.dup(fd_stdout)
        saved_stderr = os.dup(fd_stderr)
        os.dup2(fnull.fileno(), fd_stdout)
        os.dup2(fnull.fileno(), fd_stderr)
        try:
            yield
        finally:
            os.dup2(saved_stdout, fd_stdout)
            os.dup2(saved_stderr, fd_stderr)

# === ENV ===
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
APIVOID_KEY = os.getenv("APIVOID_KEY")

# === HELPERS ===
def load_email(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".eml":
        with open(path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        subject = msg.get('subject', "")
        sender = msg.get('from', "")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body += part.get_content()
        else:
            body = msg.get_content()
    elif ext == ".msg":
        msg = extract_msg.Message(path)
        subject = msg.subject or ""
        sender = msg.sender or ""
        body = msg.body or ""
    else:
        raise ValueError("Unsupported file type")
    return subject.strip(), body.strip(), sender.strip()

def check_typo_squatting(address):
    domain = address.split('@')[-1]
    common_brands = ["microsoft", "google", "apple", "amazon", "paypal", "facebook", "linkedin", "outlook", "gmail", "poste"]
    root = domain.split(".")[0].split("-")[0] if domain else ""
    for brand in common_brands:
        if fuzz.ratio(root, brand) >= 85:
            print(f"⚠️ Typosquatting: '{domain}' resembles '{brand}'")
            return 1.0
    return 0.0

def check_apivoid_links(text):
    if not APIVOID_KEY:
        return 0.0
    urls = re.findall(r'(https?://\S+)', text)
    score = 0.0
    for url in urls:
        try:
            r = requests.get(f"https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/?key={APIVOID_KEY}&url={url}")
            data = r.json()
            if data['data']['report']['blacklists']['detections'] > 0:
                score += 0.5
        except:
            continue
    return min(score, 1.0)

def contains_suspicious_words(text):
    keywords = ["urgent", "verify", "update", "click", "login", "password"]
    hits = sum(1 for kw in keywords if kw in text.lower())
    return min(hits * 0.2, 1.0)

# === MAIN ===
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--show", nargs="*", choices=["subject", "body", "headers", "sender", "all"], help="Show selected parts of the email")
parser.add_argument("file", help="Email file path")
parser.add_argument("--mode", choices=["basic", "advanced"], default="basic")
args = parser.parse_args()
show_parts = args.show or []

try:
    subject, raw_body, sender = load_email(args.file)
    soup = BeautifulSoup(raw_body, "html.parser")
    clean_body = soup.get_text(separator=" ", strip=True)

    if "all" in show_parts or "subject" in show_parts:
        print("\n--- SUBJECT ---\n" + subject)
    if "all" in show_parts or "body" in show_parts:
        print("\n--- BODY ---\n" + clean_body)
    if "all" in show_parts or "headers" in show_parts or "sender" in show_parts:
        print("\n--- SENDER ---\n" + sender)

    combined_text = f"{subject}\n{clean_body}"

    CONFIG_FILE = "models.yaml"
    default_models = [
        ("mrm8488/bert-tiny-finetuned-sms-spam-detection", "BERT Tiny"),
        ("bhadresh-savani/bert-base-go-emotion", "Emotion Proxy"),
        ("j-hartmann/emotion-english-distilroberta-base", "Hartmann Emotion")
    ]

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        models = [
            (m.get("id"), m.get("label", m.get("id")))
            for m in data.get("models", [])
            if m.get("id")
        ]
        if not models:
            models = default_models
    except Exception:
        models = default_models

    scores = []
    labels = []

    for model_name, label in models:
        try:
            with suppress_stdout():
                tok = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
                mod = AutoModelForSequenceClassification.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
                pipe = pipeline("text-classification", model=mod, tokenizer=tok, device=-1)
            res = pipe(combined_text[:512])[0]
            lbl = res['label'].lower()
            score = res['score'] if 'spam' in lbl or lbl in ['anger', 'disgust', 'fear'] else 1 - res['score']
            tag = 'spam' if score > 0.5 else 'ham'
            scores.append(score)
            labels.append(tag)
            print(f"✅ Model {label}: {score:.2f} ({tag})")
        except Exception as e:
            scores.append(0.5)
            labels.append("error")
            print(f"⚠️ Model {label} failed. Neutral score used.")

    spam_votes = labels.count("spam")
    avg_score = round(sum(scores) / len(scores), 2)

    # Advanced logic
    critical_reasons = []
    if args.mode == "advanced":
        print("\n🔍 Advanced Analysis:")
        typo_subject = check_typo_squatting(subject)
        typo_sender = check_typo_squatting(sender)
        typo_score = max(typo_subject, typo_sender)
        if typo_score >= 1.0:
            critical_reasons.append("typosquatting")
        apivoid_score = check_apivoid_links(combined_text)
        keyword_score = contains_suspicious_words(combined_text)

        print(f"🔠 TypoSquatting Score (subject or sender): {typo_score:.2f}")
        print(f"🌐 APIVoid Link Score: {apivoid_score:.2f}")
        print(f"📝 Suspicious Words Score: {keyword_score:.2f}")

        advanced_score = round((typo_score + apivoid_score + keyword_score) / 3, 2)
        print(f"🧠 Advanced Score: {advanced_score:.2f}")

        if advanced_score == 0.0:
            print("⚪ Nessun segnale avanzato rilevato. Verrà usato solo lo score basic per la valutazione finale.")

        if critical_reasons:
            reason_text = ", ".join(critical_reasons)
            print(f"🔴 Critical indicator detected ({reason_text}): forcing score to 1.0")
            combined_score = 1.0
        else:
            combined_score = round((avg_score + advanced_score) / 2, 2)
    else:
        combined_score = avg_score

    if combined_score == 1.0:
        verdict = "Phishing"
    elif spam_votes >= 2 or avg_score > 0.6:
        verdict = "Phishing"
    elif spam_votes == 1 or avg_score > 0.4 or max(scores) > 0.4:
        verdict = "Suspicious"
    else:
        verdict = "Legitimate"

    print(f"\n📊 Final Score: {combined_score:.2f} → {verdict}")
    print(f"→ Based on {spam_votes} spam votes out of {len(models)}")

except Exception as e:
    with open("error_log.txt", "w", encoding="utf-8") as f:
        f.write("=== ERROR LOG ===\n")
        f.write(traceback.format_exc())
    print("❌ Fatal error. Check error_log.txt.")
