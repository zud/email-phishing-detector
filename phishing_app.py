# phishing_app_gui.py – Streamlit GUI (Aligned with CLI Logic)

import os
import streamlit as st
import mailparser
import extract_msg
from transformers import pipeline, AutoTokenizer
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import requests
import re

# === LOAD ENV VARIABLES ===
load_dotenv()
API_KEY_APIVOID = os.getenv("APIVOID_API_KEY", "")
PHISHTANK_API_KEY = os.getenv("PHISHTANK_API_KEY", "")

# === HELPER FUNCTIONS ===
def extract_domain(email):
    return email.split("@")[-1].lower().strip(" >") if "@" in email else ""

def extract_urls(text):
    return re.findall(r'https?://\S+', text)

def clean_url(url):
    return url.strip('>"\' ')

def check_typosquatting(domain):
    common_brands = ["microsoft", "google", "apple", "amazon", "paypal", "facebook", "linkedin", "outlook", "gmail", "poste"]
    root = domain.split(".")[0].split("-")[0] if domain else ""
    for brand in common_brands:
        if fuzz.ratio(root, brand) >= 85:
            return brand
    return None

def check_domain_reputation(domain):
    if not API_KEY_APIVOID:
        return "API key not set"
    try:
        url = f"https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key={API_KEY_APIVOID}&host={domain}"
        r = requests.get(url)
        data = r.json()
        detections = data.get("data", {}).get("report", {}).get("blacklists", {}).get("detections", 0)
        return detections
    except:
        return "error"

def check_phishtank_url(url):
    if not PHISHTANK_API_KEY:
        return "API key not set"
    try:
        r = requests.post(
            "https://checkurl.phishtank.com/checkurl/",
            data={"url": url, "format": "json", "app_key": PHISHTANK_API_KEY},
            headers={"User-Agent": "phishing_gui/1.0"}
        )
        res = r.json()
        if res['results']['in_database'] and res['results']['valid']:
            return True
        return False
    except:
        return "error"

# === MODEL LOADING ===
@st.cache_resource(show_spinner=False)
def load_model():
    classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")
    return classifier, tokenizer

classifier, tokenizer = load_model()

# === STREAMLIT INTERFACE ===
st.set_page_config(page_title="Phishing Email Analyzer", layout="wide")
st.title("📧 Phishing Detection – GUI")

uploaded_file = st.file_uploader("Upload an .eml or .msg email file", type=["eml", "msg"])
mode = st.radio("Select detection mode", ["Basic", "Advanced"])

if uploaded_file:
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    subject = body = sender = return_path = ""

    if ext == ".eml":
        raw = uploaded_file.read().decode("utf-8", errors="ignore")
        parsed = mailparser.parse_from_string(raw)
        subject = parsed.subject
        body = parsed.body
        sender = parsed.from_[0][1] if parsed.from_ else ""
        return_path = parsed.return_path[0] if parsed.return_path else ""
    elif ext == ".msg":
        msg = extract_msg.Message(uploaded_file)
        subject = msg.subject
        body = msg.body
        sender = msg.sender or ""
        return_path = ""

    st.subheader("Subject")
    st.code(subject)
    st.subheader("Sender")
    st.code(sender)
    st.subheader("Body")
    st.text_area("Email content", body, height=200)

    # AI score
    inputs = tokenizer(body, truncation=True, max_length=512)
    decoded = tokenizer.decode(inputs["input_ids"], skip_special_tokens=True)
    result = classifier(decoded)
    ai_score = result[0]['score'] if result[0]['label'] == 'LABEL_1' else 1 - result[0]['score']
    st.markdown(f"**🤖 AI Score (BERT)**: `{ai_score:.2f}`")

    if mode == "Advanced":
        header_score = 0.0
        header_score_valid = False
        typos_flag = False
        phish_flag = False

        sender_domain = extract_domain(sender)
        return_domain = extract_domain(return_path)
        st.markdown(f"**🔍 Sender domain:** `{sender_domain}`")
        st.markdown(f"**🔍 Return-Path domain:** `{return_domain}`")

        if sender_domain:
            rep = check_domain_reputation(sender_domain)
            if isinstance(rep, int):
                header_score += min(rep / 5, 1.0)
                header_score_valid = True
                st.markdown(f"**🌐 APIVoid detections**: `{rep}`")
            elif rep == "API key not set":
                st.warning("APIVoid API key not configured.")

        if sender_domain and return_domain and sender_domain != return_domain:
            header_score += 0.5
            header_score_valid = True
            st.warning("⚠️ Mismatch between sender and Return-Path domains")

        typos = check_typosquatting(sender_domain)
        if typos:
            typos_flag = True
            st.warning(f"⚠️ Typosquatting detected: resembles `{typos}`")

        urls = extract_urls(body)
        if urls:
            with st.expander("🔗 Check embedded URLs (PhishTank)"):
                for url in urls:
                    cleaned = clean_url(url)
                    check = check_phishtank_url(cleaned)
                    if check is True:
                        phish_flag = True
                        st.error(f"Phishing URL detected: {cleaned}")
                        break
                    elif check == False:
                        st.success(f"Clean URL: {cleaned}")
                    elif check == "API key not set":
                        st.warning("PhishTank API key not configured.")
                        break
                    else:
                        st.warning(f"Could not check: {cleaned}")
        else:
            st.info("No URLs found in email body.")

        header_score = min(header_score, 1.0)

        critical_flags = []
        if typos_flag:
            critical_flags.append("typosquatting")
        if phish_flag:
            critical_flags.append("phishtank URL match")

        if critical_flags:
            final_score = 1.0
            st.error(f"🔴 Critical indicator detected ({', '.join(critical_flags)}): forcing score to 1.0")
        elif header_score_valid:
            final_score = round(0.6 * ai_score + 0.4 * header_score, 2)
        else:
            final_score = round(ai_score, 2)

        st.markdown(f"**🧠 Header Score**: `{header_score:.2f}`")
    else:
        final_score = round(ai_score, 2)

    label = "Phishing" if final_score >= 0.65 else "Legitimate"
    st.subheader("📊 Final Result")
    st.success(f"**{label}** with final score `{final_score}`")