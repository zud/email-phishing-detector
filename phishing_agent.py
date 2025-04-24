
# FASE 1: LOCAL PROTOTYPE – EMAIL PHISHING DETECTION

# Required libraries: pip install mail-parser extract-msg transformers torch

import os
import mailparser
import extract_msg
from transformers import pipeline, AutoTokenizer

email_path = "examples/sample_email.eml"
type_ext = os.path.splitext(email_path)[1].lower()

if type_ext == ".eml":
    parsed = mailparser.parse_from_file(email_path)
    subject = parsed.subject
    body = parsed.body
elif type_ext == ".msg":
    msg = extract_msg.Message(email_path)
    subject = msg.subject
    body = msg.body
else:
    raise ValueError("Unsupported file type. Use .eml or .msg")

print("--- SUBJECT ---")
print(subject)
print("\n--- BODY ---")
print(body)

classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-sms-spam-detection")

inputs = tokenizer(body, truncation=True, max_length=512)
decoded_input = tokenizer.decode(inputs["input_ids"], skip_special_tokens=True)

result = classifier(decoded_input)
label = result[0]['label']
score = result[0]['score']
print(f"\nResult: {label} (confidence: {score:.2f})")

with open("analysis_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Subject: {subject}\n")
    f.write(f"Label: {label} (confidence: {score:.2f})\n")
