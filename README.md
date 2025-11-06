# 🧰 Multi Tools (SteamID • QR • Photo Saver)

> 🌍 *9 dilli çoklu araç platformu:* **TR · AZ · EN-US · PT-BR · ES · RU · DE · FR · SA**  
> 🎯 *Hepsi tek bir Streamlit uygulamasında birleşti!*

---

## 💡 Genel Bakış
Multi Tools, üç mini yardımcı aracı tek sayfada toplar:

1️⃣ **SteamID Finder**  
2️⃣ **QR Code Generator**  
3️⃣ **Photo Saver (Bulk Image Downloader)**  

Hepsi sade, çok dilli, mobil uyumlu bir Streamlit arayüzünde birleşir.  

---

## 🌐 Dil Desteği
| Bayrak | Dil | Kod |
|:--:|:--|:--:|
| 🇹🇷 | Türkçe | `tr` |
| 🇦🇿 | Azərbaycan | `az` |
| 🇬🇧 | English (US) | `en` |
| 🇧🇷 | Português (Brasil) | `pt-br` |
| 🇪🇸 | Español | `es` |
| 🇷🇺 | Русский | `ru` |
| 🇩🇪 | Deutsch | `de` |
| 🇫🇷 | Français | `fr` |
| 🇸🇦 | العربية | `sa` |

---

## 🧩 Özellikler
### 🎮 SteamID Finder
- Profil bağlantısı, kullanıcı adı (vanity) veya SteamID64 girin.  
- Kullanıcı bilgilerini (isim, seviye, avatar, profil çerçevesi) çeker.  
- Gereklilik: 🔑 **`STEAM_API_KEY`** ortam değişkeni.

### 📷 QR Code Generator
- Herhangi bir metin veya URL’den anında QR kodu oluşturur.  
- ✅ Koyu/açık tema uyumu.  
- 💾 Tek tıkla indirme.

### 🖼️ Photo Saver (Bulk)
- Birden fazla görsel bağlantısını yapıştırın → ZIP olarak indirin.  
- 🔍 Imgur, meta (`og:image` / `twitter:image`) desteği.  
- 💡 Hata yönetimi ve ilerleme çubuğu içerir.

---

## ⚙️ Kurulum / Installation

### 🔧 Yerel Çalıştırma
```bash
git clone https://github.com/<kullanıcı_adın>/multi-tools.git
cd multi-tools
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# (İsteğe bağlı) Steam için:
export STEAM_API_KEY=your_key_here  # Windows PowerShell: $env:STEAM_API_KEY="your_key_here"
streamlit run app.py
```

### 🐳 Docker (opsiyonel)
```
docker build -t multi-tools .
docker run -p 8501:8501 -e STEAM_API_KEY=your_key_here multi-tools
```

### 🧠 Teknolojiler
| Araç         | Teknoloji                       |
| ------------ | ------------------------------- |
| UI Framework | 🧱 Streamlit                    |
| QR Engine    | 🌀 qrcode / Pillow              |
| Steam API    | 🎮 Steam Web API                |
| Downloader   | 🕸️ requests / aiohttp          |
| Çok Dillilik | 🌐 gettext + JSON dil dosyaları |

### ✨ Görseller
| SteamID Finder | QR Generator | Photo Saver |
| :------------: | :----------: | :---------: |
|       🎮       |      🔳      |     🖼️     |

### 📜 Lisans
Bu proje [MIT Lisansı](LICENSE) altında yayımlanmıştır.
🧑‍💻 Katkıda bulunmaktan çekinme! Pull request’ler memnuniyetle karşılanır.

💻 [GitHub Issues](https://github.com/sinan-keskin/public-all-in-one/issues)   
🌐 [Website](https://all-in-public.streamlit.app/)

⭐ Proje hoşuna gittiyse bir yıldız bırak!
Senin desteğin açık kaynak dünyasında büyük fark yaratır 🚀
