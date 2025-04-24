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
https://github.com/zud/email-phishing-detector/phishing-agent.git
cd phishing-agent

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📨 How to Use

1. Place a `.eml` or `.msg` email file in the project directory
2. Edit the file path inside `phishing_agent.py` if needed
3. Run the script:
```bash
python phishing_agent.py
```
4. Review the output in the terminal and in the `analysis_result.txt` file

---

## 📁 Project Structure
```
phishing-agent/
├── phishing_agent.py         # Main script
├── requirements.txt          # Dependencies
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
├── examples/                 # Example emails
│   ├── sample_email.eml
│   └── sample_email.msg
├── docs/                     # Deployment and usage docs
│   └── guida_deploy.md
├── screenshots/              # Visuals for README
│   └── demo_terminal.png
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
- Analysis of headers and suspicious links
- Web dashboard via Streamlit
- Outlook/Thunderbird plugin

---

![MIT License](https://img.shields.io/badge/license-MIT-green.svg)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![Status](https://img.shields.io/badge/status-working-brightgreen)
