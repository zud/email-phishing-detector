# phishing_agent_with_phishtank.py – Command-Line Phishing Analyzer (Stable Version without DNSTwist)

import os
import re
import mailparser
import extract_msg
import requests
import argparse
from transformers import pipeline, AutoTokenizer
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

# === ENV SETUP ===
load_dotenv()
API_KEY_APIVOID = os.getenv("APIVOID_API_KEY", "")
PHISHTANK_API_KEY = os.getenv("PHISHTANK_API_KEY", "")

# === ARGPARSE ===
parser = argparse.ArgumentParser(description="Phishing detection script with PhishTank integration")
parser.add_argument("file", help="Path to .eml or .msg email file")
parser.add_argument("--mode", choices=["basic", "advanced"], default="basic", help="Analysis mode")
args = parser.parse_args()

email_path = args.file
use_advanced = args.mode == "advanced"

ext = os.path.splitext(email_path)[1].lower()

# === EMAIL PARSING ===
if ext == ".eml":
    with open(email_path, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")
    parsed = mailparser.parse_from_string(content)
    subject = parsed.subject
    body = parsed.body
    sender = parsed.from_[0][1] if parsed.from_ else ""
    return_path = parsed.return_path[0] if parsed.return_path else ""
elif ext == ".msg":
    msg = extract_msg.Message(email_path)
    subject = msg.subject
    body = msg.body
    sender = msg.sender or ""
    return_path = ""
else:
    raise ValueError("Unsupported file type. Use .eml or .msg")

print("--- SUBJECT ---\n", subject)
print("\n--- BODY ---\n", body)
print("\n--- SENDER ---\n", sender)
print("--- RETURN PATH ---\n", return_path)

# === BERT AI DETECTION ===
classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")

inputs = tokenizer(body, truncation=True, max_length=512)
decoded_input = tokenizer.decode(inputs["input_ids"], skip_special_tokens=True)
result = classifier(decoded_input)
ai_score = result[0]['score'] if result[0]['label'] == 'LABEL_1' else 1 - result[0]['score']

# === HELPERS ===
def extract_domain(email):
    return email.split("@")[-1].lower().strip(" >") if "@" in email else ""

def extract_urls(text):
    return re.findall(r'https?://\S+', text)

def clean_url(url):
    return url.strip('>"\' ')

def check_domain_reputation(domain):
    if not API_KEY_APIVOID:
        print("ℹ️ APIVoid API key not set. Domain reputation checks are disabled.")
        return 0.0
    try:
        url = f"https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key={API_KEY_APIVOID}&host={domain}"
        r = requests.get(url)
        data = r.json()
        detections = data.get("data", {}).get("report", {}).get("blacklists", {}).get("detections", 0)
        print(f"APIVoid score for {domain}: {detections} detections")
        return min(detections / 5, 1.0)
    except:
        return 0.0

def check_typosquatting(domain):
    common_brands = ["microsoft", "google", "apple", "amazon", "paypal", "facebook", "linkedin", "outlook", "gmail", "poste"]
    root = domain.split(".")[0].split("-")[0] if domain else ""
    for brand in common_brands:
        if fuzz.ratio(root, brand) >= 85:
            print(f"⚠️ Typosquatting: '{domain}' resembles '{brand}'")
            return True
    return False

def check_phishtank_url(url):
    if not PHISHTANK_API_KEY:
        print("ℹ️ PhishTank API key not set. URL reputation checks are disabled.")
        return False
    try:
        r = requests.post(
            "https://checkurl.phishtank.com/checkurl/",
            data={"url": url, "format": "json", "app_key": PHISHTANK_API_KEY},
            headers={"User-Agent": "phishing_agent/1.0"}
        )
        res = r.json()
        if res['results']['in_database']:
            if res['results']['valid']:
                print(f"⚠️ PhishTank reports phishing for: {url}")
                return True
            else:
                print(f"✅ URL checked: {url} is not a valid phishing report in PhishTank.")
        else:
            print(f"✅ URL checked: {url} not found in PhishTank database.")
    except:
        print(f"⚠️ Could not check PhishTank for URL: {url}")
    return False

# === ADVANCED ANALYSIS ===
sender_domain = extract_domain(sender)
return_domain = extract_domain(return_path)
header_score = 0.0
header_score_valid = False
typosquatting_flag = False
phishtank_flag = False

if use_advanced:
    print(f"Sender domain: {sender_domain}")
    print(f"Return-Path domain: {return_domain}")

    if not API_KEY_APIVOID:
        print("⚠️ APIVoid: API key not provided. This feature is inactive in advanced mode.")
    if not PHISHTANK_API_KEY:
        print("⚠️ PhishTank: API key not provided. This feature is inactive in advanced mode.")

    if sender_domain:
        rep_score = check_domain_reputation(sender_domain)
        if rep_score > 0:
            header_score += rep_score
            header_score_valid = True

    if sender_domain and return_domain and sender_domain != return_domain:
        print("⚠️ Mismatch between sender and return-path")
        header_score += 0.5
        header_score_valid = True

    if check_typosquatting(sender_domain):
        typosquatting_flag = True

    urls = extract_urls(body)
    if urls:
        print("\n🔎 Checking URLs against PhishTank...")
        for url in urls:
            cleaned = clean_url(url)
            if check_phishtank_url(cleaned):
                phishtank_flag = True
                break
    else:
        print("ℹ️ No URLs found in email body for PhishTank checking.")

    header_score = min(header_score, 1.0)

# === FINAL SCORE ===
if use_advanced:
    critical_reasons = []
    if typosquatting_flag:
        critical_reasons.append("typosquatting")
    if phishtank_flag:
        critical_reasons.append("phishtank URL match")

    if critical_reasons:
        reason_text = ", ".join(critical_reasons)
        print(f"🔴 Critical indicator detected ({reason_text}): forcing score to 1.0")
        final_score = 1.0
    elif header_score_valid:
        final_score = round(0.6 * ai_score + 0.4 * header_score, 2)
    else:
        final_score = round(ai_score, 2)
else:
    final_score = round(ai_score, 2)

label = "Phishing" if final_score >= 0.65 else "Legitimate"

# === OUTPUT ===
print(f"\nAI score: {ai_score:.2f}")
if use_advanced:
    print(f"Header score: {header_score:.2f}")
print(f"Final score: {final_score} → {label}")

with open("analysis_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Subject: {subject}\n")
    f.write(f"Sender: {sender}\n")
    f.write(f"Return-Path: {return_path}\n")
    f.write(f"AI Score: {ai_score:.2f}\n")
    if use_advanced:
        f.write(f"Header Score: {header_score:.2f}\n")
        f.write(f"Typosquatting: {typosquatting_flag}\n")
        f.write(f"PhishTank URL Match: {phishtank_flag}\n")
    f.write(f"Final Score: {final_score} → {label}\n")
