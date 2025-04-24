import streamlit as st
import mailparser
import extract_msg
from transformers import pipeline, AutoTokenizer
import os

st.set_page_config(page_title="Phishing Agent GUI", page_icon="🛡️")

st.title("📥 Phishing Email Analyzer")
st.write("Upload a `.eml` or `.msg` file to detect phishing content using AI and optional header analysis.")

uploaded_file = st.file_uploader("Choose an email file", type=["eml", "msg"])

if uploaded_file:
    ext = os.path.splitext(uploaded_file.name)[-1].lower()
    subject = ""
    body = ""
    sender = ""
    if ext == ".eml":
        parsed = mailparser.parse_from_file_obj(uploaded_file)
        subject = parsed.subject
        body = parsed.body
        sender = parsed.from_[0][1] if parsed.from_ else ""
    elif ext == ".msg":
        with open("temp.msg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        msg = extract_msg.Message("temp.msg")
        subject = msg.subject
        body = msg.body
        sender = msg.sender

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
    label = result[0]['label']
    score = result[0]['score']

    st.markdown(f"**Result:** `{label}` with confidence `{score:.2f}`")
