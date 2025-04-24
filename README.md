# 🛡️ Phishing Agent – Email Classifier

A lightweight, local, open-source tool to detect suspicious emails (phishing or spam) in `.eml` and `.msg` formats using a BERT Tiny-based AI model. Now optionally enhanced with domain reputation and header analysis.

---

## 🚀 Features
- Local analysis (no data sent externally by default)
- Supports `.eml` and `.msg` (Outlook) email formats
- Spam / legitimate classification using a fine-tuned BERT model
- Optional advanced mode:
  - Mismatch detection (From vs Return-Path)
  - Reputation check via [APIVoid](https://www.apivoid.com)
- Clear output in terminal and `.txt` file

---

## 🧠 AI Model Used
- **Model:** `mrm8488/bert-tiny-finetuned-sms-spam-detection`
- **Type:** BERT Tiny
- **Task:** Binary classification: spam vs. not spam
- **Highlights:**
  - Runs locally on CPU
  - No cloud processing needed for base detection

---

## ⚙️ Installation

### 🔧 Prerequisites
- Python 3.10+
- Virtual environment (recommended)

```bash
# Clone the repository
https://github.com/your-username/phishing-agent.git
cd phishing-agent

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 📨 How to Use

### Base mode (BERT only):
```python
USE_ADVANCED_ANALYSIS = False
```

### Advanced mode (headers + domain reputation):
1. Create a `.env` file from `.env.example`
2. Add your APIVoid API key:
```bash
APIVOID_API_KEY=your_real_api_key_here
```
3. In the script, set:
```python
USE_ADVANCED_ANALYSIS = True
```
4. Run the script:
```bash
python phishing_agent.py
```

---

## 📁 Project Structure
```
phishing-agent/
├── phishing_agent.py         # Main script
├── requirements.txt          # Dependencies
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
├── .env.example              # Example env file for API config
├── examples/                 # Example emails
│   ├── sample_email.eml
│   └── sample_email.msg
├── docs/                     # Deployment and usage docs
│   └── guida_deploy.md
```

---

## 🛡️ License
This project is licensed under the **MIT License**.

---

## 👤 Authors
- Alessandro Bruchi – [alessandro.bruchi@iit.it](mailto:alessandro.bruchi@iit.it)
- In collaboration with ChatGPT (OpenAI)

---

## 💡 Future Ideas
- GPT integration for ensemble decision-making
- Full dashboard via Streamlit or Electron
- Webhook notifications for alerts

---

![MIT License](https://img.shields.io/badge/license-MIT-green.svg)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![Status](https://img.shields.io/badge/status-working-brightgreen)