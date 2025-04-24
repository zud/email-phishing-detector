import streamlit as st
import mailparser
import extract_msg
from transformers import pipeline, AutoTokenizer
import os
import requests

st.set_page_config(page_title="Phishing Agent GUI", page_icon="🛡️")

st.title("📥 Phishing Email Analyzer")
st.write("Upload a `.eml` or `.msg` file to detect phishing content using AI.")

uploaded_file = st.file_uploader("Choose an email file", type=["eml", "msg"])
use_advanced = st.checkbox("Enable advanced analysis (header & domain checks)")

API_KEY_APIVOID = os.getenv("APIVOID_API_KEY", "")

if uploaded_file:
    ext = os.path.splitext(uploaded_file.name)[-1].lower()
    subject = ""
    body = ""
    sender = ""
    return_path = ""

    if ext == ".eml":
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        parsed = mailparser.parse_from_string(content)
        subject = parsed.subject
        body = parsed.body
        sender = parsed.from_[0][1] if parsed.from_ else ""
        return_path = parsed.return_path[0] if parsed.return_path else ""

    elif ext == ".msg":
        with open("temp.msg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        msg = extract_msg.Message("temp.msg")
        subject = msg.subject
        body = msg.body
        sender = msg.sender
        return_path = ""

    st.subheader("📨 Email Content")
    st.markdown(f"**Subject:** {subject}")
    st.markdown(f"**Sender:** {sender}")
    st.text_area("Body", body, height=200)

    st.subheader("🧠 AI Phishing Analysis")
    classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")

    inputs = tokenizer(body, truncation=True, max_length=512)
    decoded_input = tokenizer.decode(inputs["input_ids"], skip_special_tokens=True)
    result = classifier(decoded_input)
    ai_label = result[0]['label']
    ai_score = result[0]['score'] if ai_label == 'LABEL_1' else 1 - result[0]['score']

    header_score = 0.0

    if use_advanced:
        def extract_domain(email):
            return email.split("@")[-1].lower() if "@" in email else ""

        def check_domain_reputation(domain):
            if not API_KEY_APIVOID:
                st.warning("No APIVoid API key set. Skipping domain reputation check.")
                return 0.0
            try:
                url = f"https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key={API_KEY_APIVOID}&host={domain}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    detections = data.get("data", {}).get("report", {}).get("blacklists", {}).get("detections", 0)
                    return min(detections / 5, 1.0)
                else:
                    return 0.0
            except Exception as e:
                st.error(f"Error checking domain reputation: {e}")
                return 0.0

        sender_domain = extract_domain(sender)
        return_domain = extract_domain(return_path)

        if sender_domain and return_domain and sender_domain != return_domain:
            header_score += 0.5

        header_score += check_domain_reputation(sender_domain)
        header_score = min(header_score, 1.0)

    final_score = round(0.6 * ai_score + 0.4 * header_score, 2) if use_advanced else round(ai_score, 2)
    label = "Phishing" if final_score >= 0.65 else "Legitimate"

    st.success(f"Final phishing score: {final_score} → **{label}**")
