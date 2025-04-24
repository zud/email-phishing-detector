# 🛡️ Phishing Agent – Email Classifier

A lightweight, local, open-source tool to detect suspicious emails (phishing or spam) in `.eml` and `.msg` formats using a BERT Tiny-based AI model.

---

## 🚀 Features
- Local analysis (no data sent externally)
- Supports `.eml` and `.msg` (Outlook) email formats
- Spam / legitimate classification using a fine-tuned BERT model
- Clear output in terminal and `.txt` file

---

## 🧠 AI Model Used
- **Model:** `mrm8488/bert-tiny-finetuned-sms-spam-detection`
- **Type:** BERT Tiny
- **Task:** Binary classification: spam vs. not spam
- **Highlights:**
  - Runs locally on CPU
  - No data transmission
  - Limitation: max input 512 tokens

---

## ⚙️ Installation

### 🔧 Prerequisites
- Python 3.10+
- (Recommended) Virtual environment

```bash
# Clone the repository
https://github.com/your-username/phishing-agent.git
cd phishing-agent

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📨 How to Use

1. Place a `.eml` or `.msg` email file in the