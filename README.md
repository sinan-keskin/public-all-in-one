# 🧰 Multi Tools (SteamID • QR • Photo Saver)

> 🌍 *Multi-language tool platform:* **TR · AZ · EN-US · PT-BR · ES · RU · DE · FR · SA**  
> 🎯 *All combined into a single Streamlit application!*

---

## 💡 Overview

Multi Tools brings together three mini utilities in one interface:

1️⃣ **SteamID Finder**  
2️⃣ **QR Code Generator**  
3️⃣ **Photo Saver (Bulk Image Downloader)**  

Everything is unified in a clean, multilingual, mobile-friendly Streamlit UI.

---

## 🌐 Language Support

| Flag | Language | Code |
|:--:|:--|:--:|
| 🇹🇷 | Turkish | `tr` |
| 🇦🇿 | Azerbaijani | `az` |
| 🇬🇧 | English (US) | `en` |
| 🇧🇷 | Portuguese (Brazil) | `pt-br` |
| 🇪🇸 | Spanish | `es` |
| 🇷🇺 | Russian | `ru` |
| 🇩🇪 | German | `de` |
| 🇫🇷 | French | `fr` |
| 🇸🇦 | Arabic | `sa` |

---

## 🧩 Features

### 🎮 SteamID Finder
- Enter a profile link, Steam vanity name, or SteamID64.  
- Fetches user data (name, level, avatar, profile frame).  
- Requirement: 🔑 **`STEAM_API_KEY`** environment variable.

### 📷 QR Code Generator
- Create instant QR codes from any text or URL.  
- ✅ Dark/light theme compatible.  
- 💾 One-click download.

### 🖼️ Photo Saver (Bulk)
- Paste multiple image URLs → download them as a ZIP.  
- 🔍 Supports Imgur, meta (`og:image` / `twitter:image`) links.  
- 💡 Includes error handling and a progress bar.

---

## ⚙️ Installation

### 🔧 Run Locally
```bash
git clone https://github.com/<your_username>/multi-tools.git
cd multi-tools
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# (Optional) For Steam:
export STEAM_API_KEY=your_key_here  # Windows PowerShell: $env:STEAM_API_KEY="your_key_here"
streamlit run app.py
```

### 🐳 Docker (optional)
```docker
docker build -t multi-tools .
docker run -p 8501:8501 -e STEAM_API_KEY=your_key_here multi-tools
```

### 🧠 Technologies
| Component    | Technology                      |
| ------------ | ------------------------------- |
| UI Framework | 🧱 Streamlit                    |
| QR Engine    | 🌀 qrcode / Pillow              |
| Steam API    | 🎮 Steam Web API                |
| Downloader   | 🕸️ requests / aiohttp          |
| i18n (Locale) | 🌐 gettext + JSON language files |

### ✨ Screenshots
| SteamID Finder | QR Generator | Photo Saver |
| :------------: | :----------: | :---------: |
|       🎮       |      🔳      |     🖼️     |

![Giriş](https://image.prntscr.com/image/3AQ5lPAhRtiG4FiWzhL6xw.jpeg)

![SteamID64 Finder](https://image.prntscr.com/image/432u0iRsSZehLF02oyZtpw.jpeg)

![QR Oluşturucu](https://image.prntscr.com/image/w3coQMngR6es3n7CkOXG3g.jpeg)

![Photo Saver](https://image.prntscr.com/image/jHWjGdv7TSmYOzTyebaU8w.jpeg)


### 📜 License
This project is released under the [MIT Lisansı](LICENSE).
🧑‍💻 Contributions are welcome — pull requests are appreciated!

💻 [GitHub Issues](https://github.com/sinan-keskin/public-all-in-one/issues)   
🌐 [Website](https://all-in-public.streamlit.app/)

⭐ If you like this project, consider leaving a star!
Your support makes a huge difference in the open-source world 🚀
