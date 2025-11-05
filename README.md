# 🧰 Multi Tools (SteamID • QR • Photo Saver)

Üç mini aracı tek bir Streamlit uygulamasında sunar — **sekme sırası**:
1) `steamid-finder` · 2) `qr-code` · 3) `photo-saver`.  
Desteklenen diller: **TR / AZ / EN / PT-BR / ES / RU**.

---

## 🇹🇷 Özellikler
- **SteamID Bulucu**: Profil linki, kullanıcı adı (vanity) veya SteamID64 girin; görünen ad, seviye, avatar/çerçeve bilgilerini çeker.  
  > *API anahtarı gerekli:* `STEAM_API_KEY`.
- **QR Kod Üretici**: Girdiğiniz URL için anında QR kodu oluşturur ve indirmenizi sağlar.
- **Toplu Görsel İndirici**: Birden fazla görsel/link yapıştırın, resimleri çözüp ZIP olarak indirin. Imgur ve meta (`og:image` / `twitter:image`) çözümleri içerir.

## 🇦🇿 Xüsusiyyətlər
- **SteamID Axtarışı**, **QR Yaratma**, **Kütləvi Şəkil Endirmə** — yuxarıdakı kimi.

## 🇬🇧 Features
- **SteamID Finder**, **QR Generator**, **Bulk Image Downloader** — as above.

## 🇧🇷 Funcionalidades
- **Localizador de SteamID**, **Gerador de QR**, **Baixar Imagens em Lote** — conforme acima.

## 🇪🇸 Funciones
- **Buscador de SteamID**, **Generador de QR**, **Descargador Masivo de Imágenes**.

## 🇷🇺 Возможности
- **Поиск SteamID**, **Генератор QR**, **Массовая загрузка изображений**.

---

## 🚀 Kurulum / Setup

### 1) Yerel Çalıştırma
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# (İsteğe bağlı) Steam için:
export STEAM_API_KEY=your_key_here  # Windows PowerShell: $env:STEAM_API_KEY="your_key_here"
streamlit run app.py
