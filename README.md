# 🛡️ Phishing Agent – Email Classifier

A lightweight, local, open-source tool to detect suspicious emails (phishing or spam) in `.eml` and `.msg` formats using a BERT Tiny-based AI model. Now optionally enhanced with domain reputation and header analysis.

> ⚠️ **This project is intended for local/private use only.** Public deployment is not recommended without appropriate security and compliance assessments.

> 📩 **Commercial use or enterprise integration?** Contact: [alessandro.bruchi@iit.it](mailto:alessandro.bruchi@iit.it)

---

## 🚀 Features

- 🧠 Local AI-based classification with no cloud dependency
- 📂 Support for `.eml` and `.msg` (Outlook) email formats
- 🤖 Three operational modes:
  - **Basic**: BERT-based classification only
  - **Advanced**: Adds sender reputation (via APIVoid), typosquatting detection, and URL phishing checks (via PhishTank)
  - **GUI**: Web interface using Streamlit for file upload and analysis
- 📊 Results printed in console and saved in `analysis_result.txt`
- ✅ Optional `.env` config for API keys

---

## 🧠 AI Model Used

- **Model**: [`mrm8488/bert-tiny-finetuned-sms-spam-detection`](https://huggingface.co/mrm8488/bert-tiny-finetuned-sms-spam-detection)
- **Purpose**: Spam/phishing vs. ham (binary classification)
- **Highlights**:
  - Lightweight & fast (BERT Tiny)
  - Works locally on CPU

---

## ⚙️ Installation

### 🔧 Requirements
- Python 3.10+
- Virtual environment (recommended)

```bash
# Clone the repository
https://github.com/zud/email-phishing-detector.git
cd phishing-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Usage

### 🖥️ Command-line (CLI) modes

#### 🔹 Basic mode:
```bash
python phishing_agent.py path/to/email.eml --mode basic
```

#### 🔹 Advanced mode:
```bash
python streamlit run phishing_app.py path/to/email.msg --mode advanced
```
> Requires `.env` with your API keys for APIVoid and/or PhishTank.

### 📊 Graphical interface (GUI)
```bash
streamlit run phishing_app.py
```
Upload an email file and select the analysis mode in your browser.

---

## 📁 Project Structure
```
phishing-agent/
├── phishing_agent.py  # CLI logic with all features
├── phishing_app.py               # Streamlit GUI frontend
├── requirements.txt                  # All dependencies
├── .env.example                      # Sample environment file
├── LICENSE                           # AGPLv3 License
├── README.md                         # Project documentation
├── CHANGELOG.md                      # Release and update notes
├── examples/                         # Example email files
│   ├── sample_email.eml
│   └── sample_email.msg
├── docs/                             # Usage and deployment docs
│   └── guida_deploy.md
```

---

## 🛡️ License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPLv3)**.

See [LICENSE](LICENSE) for full terms.

---

## 👤 Author

**Alessandro Bruchi**  
[alessandro.bruchi@iit.it](mailto:alessandro.bruchi@iit.it)

> _Built in collaboration with OpenAI’s ChatGPT for architectural and implementation guidance._

---

## 💡 Future Ideas

- 🧠 GPT-based ensemble phishing evaluator
- 🔔 Email inbox monitoring (IMAP/POP)
- 📊 Dashboard via Streamlit Cloud or Hugging Face Spaces
- 🔐 DKIM/SPF/DMARC inspection module

---

![AGPL License](https://img.shields.io/badge/license-AGPL--v3-blue.svg)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen)
