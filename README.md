# 🛡️ Phishing Agent – Email Classifier

A lightweight, local, open-source tool to detect suspicious emails (phishing or spam) in `.eml` and `.msg` formats using a BERT Tiny-based AI model. Now optionally enhanced with domain reputation and header analysis.

> ⚠️ **This project is intended for local/private use only.** If you plan to deploy it as a public-facing web application, please consider the privacy risks associated with handling sensitive email content. Public deployment is not recommended without appropriate security and compliance checks.

> 📩 **Commercial use or enterprise integration?** Contact: [alessandro.bruchi@iit.it](mailto:alessandro.bruchi@iit.it)

---

## 🚀 Features
- Local analysis (no data sent externally by default)
- Supports `.eml` and `.msg` (Outlook) email formats
- Spam / legitimate classification using a fine-tuned BERT model
- Three operational modes:
  - **Base**: AI-based classification only
  - **Advanced**: Includes header and sender reputation checks (APIVoid)
  - **GUI**: Interactive drag-and-drop interface via Streamlit
- Clear output in terminal and `.txt` report

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

## 🧪 Usage

### 🖥️ Command-line (CLI) modes

#### Base mode:
```bash
python phishing_agent.py path/to/email.eml --mode basic
```

#### Advanced mode (with header analysis and domain reputation):
```bash
python phishing_agent.py path/to/email.msg --mode advanced
```

> 💡 Make sure you set your APIVoid key in a `.env` file if using advanced mode.

### 📊 Graphical interface (GUI)
```bash
streamlit run phishing_app.py
```
Upload a `.eml` or `.msg` file and the AI will analyze the content.

---

## 📁 Project Structure
```
phishing-agent/
├── phishing_agent.py         # CLI analysis script
├── phishing_app.py           # GUI interface via Streamlit
├── requirements.txt          # Dependencies
├── LICENSE                   # AGPLv3 License
├── README.md                 # Project documentation
├── .env.example              # Example env file for API config
├── CHANGELOG.md              # Version history and license info
├── examples/                 # Example emails
│   ├── sample_email.eml
│   └── sample_email.msg
├── docs/                     # Deployment and usage docs
│   └── guida_deploy.md
```

---

## 🛡️ License
This project is licensed under the **GNU Affero General Public License v3.0 (AGPLv3)**. See [LICENSE](LICENSE) for more information.

---

## 👤 Authors
- Alessandro Bruchi – [alessandro.bruchi@iit.it](mailto:alessandro.bruchi@iit.it)

_This project was developed with the assistance of OpenAI’s ChatGPT, which provided non-binding suggestions during implementation._

---

## 💡 Future Ideas
- GPT integration for ensemble decision-making
- Email inbox watcher with automated checks
- Full dashboard with Streamlit Cloud or Hugging Face Spaces

---

![AGPL License](https://img.shields.io/badge/license-AGPL--v3-blue.svg)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen)