# 🚀 Vuln-Watch

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Vuln-Watch** is a minimalist, fast, and automated Cyber Threat Intelligence (CTI) tool designed for security researchers and bug bounty hunters. It continuously monitors the **NVD (National Vulnerability Database)** and **GitHub PoC/Exploit repositories** based on your custom keywords (e.g., *HyperOS, Android RCE, Linux Kernel*), delivering real-time intelligence directly to your terminal or Telegram channel.

---

## ✨ Features

- 🔍 **Multi-Source Intelligence:** Tracks both official CVE publications (NVD) and fresh open-source exploits (GitHub).
- 📊 **Beautiful Terminal UI:** Uses `Rich` library to print clean, color-coded threat intelligence tables.
- 🚫 **Smart Deduplication:** Keeps track of previously seen items via `seen_items.json` so you never get spammed with the same vulnerability twice.
- 🔔 **Instant Alerts:** Optional Telegram Bot integration to send critical zero-day discoveries straight to your pocket.

---

## 🛠️ Installation & Setup

Since this tool is designed to be lightweight, setting it up on Kali Linux, Ubuntu, or any VPS takes less than a minute.

### 1. Clone the Repository
```bash
git clone git@github.com:apo536098-wq/vuln-watch.git
cd vuln-watch

---

#### 2. Create a Virtual Environment & Install Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

---

##### ⚙️ Configuration (config.json)
#You can easily customize your watchlists and notification settings without touching the core code. Edit config.json:

{
    "keywords": ["HyperOS", "Android RCE", "Linux Kernel", "Xiaomi"],
    "telegram_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
    "check_interval_minutes": 5
}


#Note: If you leave the Telegram fields as default, the tool will gracefully skip mobile notifications and only print to the terminal.


######🚀 Usage
#To spin up the intelligence engine, simply run:

python3 vuln_watch.py


#📝 License
This project is licensed under the MIT License - feel free to modify, share, and use it in your professional red/blue team operations.

Developed with 🛡️ by apo536098-wq
