import streamlit as st
import subprocess
import os
import sys

st.set_page_config(page_title="Phishing Detector", page_icon="📩")
st.title("📩 Phishing Detector v1.3.0 (Advanced)")

uploaded_file = st.file_uploader("Upload an email file (.eml or .msg)", type=["eml", "msg"])

mode = st.radio("Select analysis mode", ["basic", "advanced"], index=1)

if uploaded_file:
    # Save the uploaded file temporarily
    temp_dir = "temp_emails"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("🕵️ Analyze"):
        with st.spinner("Analyzing email..."):
            command = [sys.executable, "phishing_agent.py", file_path, "--mode", mode]
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')

        st.subheader("📋 Analysis Results")
        if result.stdout:
            st.code(result.stdout, language="bash")

        if result.stderr:
            st.error("⚠️ Errors detected:")
            st.code(result.stderr)

        # Clean up temp file
        try:
            os.remove(file_path)
        except Exception as e:
            st.warning(f"Could not delete temp file: {e}")
