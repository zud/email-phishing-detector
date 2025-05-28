# 🛡️ Phishing Agent – Email Classifier

A lightweight, local, open-source tool to detect suspicious emails (phishing or spam) in `.eml` and `.msg` formats using a BERT Tiny-based AI model. Now optionally enhanced with domain reputation and header analysis.
**Current Version: 1.4.0** – see the [Changelog](Changelog) for release notes.

> ⚠️ **This project is intended for local/private use only.** Public deployment is not recommended without appropriate security and compliance assessments.

> 📩 **Commercial use or enterprise integration?** Contact: [alessandro.bruchi@iit.it](mailto:alessandro.bruchi@iit.it)



# 📩 Email Phishing Detector

## Overview

Email Phishing Detector is a tool designed to detect phishing emails by analyzing the subject and body of `.eml` or `.msg` files. It supports both basic AI ensemble and advanced checks such as typo-squatting and suspicious URLs.

## ✨ What's new in 1.4.0

- Full refactoring of `phishing_agent.py`.
- **Basic Mode**: loads an ensemble of models from `models.yaml` (default set below):
  - `mrm8488/bert-tiny-finetuned-sms-spam-detection`
  - `bhadresh-savani/bert-base-go-emotion`
  - `j-hartmann/emotion-english-distilroberta-base`
- Recalculated ensemble scoring logic.
- Added Hugging Face token management via `.env`.
- Added `models.yaml` for customizable model configuration.
- **Advanced Mode**: typo-squatting detection (fuzzy match >= 85%), APIVoid link scanning, and critical reason forcing to phishing.
- **Streamlit GUI**: drag & drop support, inherits CLI logic, ready for cloud deployment.
- Added deployment guide under `docs/`.
- **Licensing**: AGPLv3. Note that AI models may have separate Hugging Face licenses.

---

## 🚀 Features

- 🧠 Local AI-based classification with no cloud dependency
- 📂 Support for `.eml` and `.msg` (Outlook) email formats
- 🤖 Three operational modes:
  - **Basic**: AI-based classification only
  - **Advanced**: Adds sender reputation (via APIVoid), typosquatting detection
  - **GUI**: Web interface using Streamlit for file upload and analysis
- 📊 Results printed in console and saved in `analysis_result.txt`
- ✅ Optional `.env` config for API keys

---

## 🧠 AI Models

The agent loads one or more models defined in `models.yaml`. By default it uses:
- `mrm8488/bert-tiny-finetuned-sms-spam-detection`
- `bhadresh-savani/bert-base-go-emotion`
- `j-hartmann/emotion-english-distilroberta-base`

### Adding or replacing models

Edit `models.yaml` to customize the ensemble. Each entry requires an `id` and a
`label`. For example, you can replace a model with multilingual support using
`xlm-roberta-base`:

```yaml
models:
  - id: xlm-roberta-base
    label: XLM-RoBERTa
```

The agent will load the updated list at the next run.

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


### CLI Version

```bash
python phishing_agent.py path_to_email.eml --mode advanced --show all
```

### Streamlit GUI Version

```bash
python -m streamlit run phishing_app.py
```

## 🔑 Environment Variables

- `HUGGINGFACE_TOKEN` — Hugging Face API token for private/gated models.
- `APIVOID_KEY` — (optional) API key for APIVoid URL reputation checking.



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

- This project is licensed under **AGPLv3**.
- **Important**: The Hugging Face models used (`bert-tiny`, `go-emotion`, `distilroberta-base`) may have additional specific licenses. Ensure compliance when using the models.


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
