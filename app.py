# -*- coding: utf-8 -*-
import os, io, re, json, zipfile, requests
from datetime import datetime
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components

# ------- Optional deps (Photo Saver) -------
try:
    import cloudscraper
    from bs4 import BeautifulSoup
    HAVE_SCRAPER = True
    scraper = cloudscraper.create_scraper()
except Exception:
    HAVE_SCRAPER = False
    scraper = requests  # graceful fallback

# ------- Optional deps (QR) -------
try:
    from PIL import Image
    from io import BytesIO
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

# ================== App Config ==================
st.set_page_config(page_title="🧰 Multi Tools", page_icon="🧰", layout="centered")

# ================== i18n ==================
I18N = {
    "tr": {
        "page_title": "Multi Tools (SteamID • QR • Görsel)",
        "lang_label": "Dil",
        "tabs_titles": ["SteamID64 Bulucu", "Karekod Oluşturucu", "Görsel Kaydedici"],

        # Steam
        "steam_title": "🎮 SteamID Bulucu",
        "steam_caption": "Profil linki, kullanıcı adı (vanity) veya SteamID64 ile bilgileri getirir.",
        "steam_input": "Profil URL'si, Kullanıcı Adı (vanity) veya SteamID64",
        "steam_ph": "Örn: https://steamcommunity.com/id/gaben | gaben | 7656...",
        "steam_btn": "Ara",
        "steam_found": "Bulundu!",
        "steam_warn_api": "⚠️ Lütfen `STEAM_API_KEY` secret/ENV ekleyin.",
        "steam_display": "Görünen Kullanıcı Adı",
        "steam_username": "Kullanıcı Adı",
        "steam_sid64": "SteamID64",
        "steam_level": "Seviye",
        "copy": "Kopyala",
        "copied": "Kopyalandı!",
        "copy_failed": "Kopyalama başarısız: ",

        # QR
        "qr_title": "🔗 URL'den QR Kod Oluştur",
        "qr_caption": "Girdiğiniz URL için anında QR kodu üretin.",
        "qr_input": "URL",
        "qr_ph": "https://example.com",
        "qr_btn": "QR Oluştur",
        "qr_warn": "Lütfen önce bir URL girin.",
        "qr_error": "Bir hata oluştu: ",
        "qr_download": "⤓ QR Kodunu İndir",
        "qr_preview": "🔍 Oluşan QR Kodu",

        # Photo Saver
        "ps_title": "📥 Toplu Görsel İndirici",
        "ps_caption": "Bağlantıları yapıştırın, resimleri ZIP olarak indirin.",
        "ps_area": "Görsel URL'lerini alt alta yapıştırın:",
        "ps_btn": "ZIP Oluştur",
        "ps_need": "Lütfen en az bir URL girin.",
        "ps_ready": "{} resim algılandı, ZIP dosyanız hazır.",
        "ps_dl": "ZIP dosyasını indir",
        "ps_errorlog": "error_log.txt",
        "footer_tip": "Alt kısımdaki simgeler popüler görsel servislerine gider.",

        # Footer
        "footer_contact": "Hata & Öneriler için",
    },
    "az": {
        "page_title": "Multi Tools (SteamID • QR • Şəkil)",
        "lang_label": "Dil",
        "tabs_titles": ["SteamID64 Axtarıcı", "QR Kod Yaradıcı", "Şəkil Yükləyici"],

        "steam_title": "🎮 SteamID Axtarışı",
        "steam_caption": "Profil linki, istifadəçi adı (vanity) və ya SteamID64 ilə məlumat gətirir.",
        "steam_input": "Profil URL-i, İstifadəçi Adı (vanity) və ya SteamID64",
        "steam_ph": "Məs.: https://steamcommunity.com/id/gaben | gaben | 7656...",
        "steam_btn": "Axtar",
        "steam_found": "Tapıldı!",
        "steam_warn_api": "⚠️ Zəhmət olmasa `STEAM_API_KEY` secret/ENV əlavə edin.",
        "steam_display": "Görünən Ad",
        "steam_username": "İstifadəçi Adı",
        "steam_sid64": "SteamID64",
        "steam_level": "Səviyyə",
        "copy": "Kopyala",
        "copied": "Kopyalandı!",
        "copy_failed": "Kopyalama alınmadı: ",

        "qr_title": "🔗 URL-dən QR Kod Yarat",
        "qr_caption": "Daxil etdiyiniz URL üçün dərhal QR yaradın.",
        "qr_input": "URL",
        "qr_ph": "https://example.com",
        "qr_btn": "QR Yarat",
        "qr_warn": "Zəhmət olmasa əvvəlcə URL daxil edin.",
        "qr_error": "Xəta baş verdi: ",
        "qr_download": "⤓ QR Kodunu Endir",
        "qr_preview": "🔍 Yaradılan QR Kod",

        "ps_title": "📥 Kütləvi Şəkil Endirici",
        "ps_caption": "Linkləri yapışdırın, şəkilləri ZIP kimi endirin.",
        "ps_area": "Şəkil URL-lərini alt-alta yapışdırın:",
        "ps_btn": "ZIP Yarat",
        "ps_need": "Zəhmət olmasa ən az bir URL daxil edin.",
        "ps_ready": "{} şəkil aşkarlandı, ZIP faylınız hazırdır.",
        "ps_dl": "ZIP faylını endir",
        "ps_errorlog": "error_log.txt",
        "footer_tip": "Aşağıdakı ikonlar məşhur şəkil servislərinə aparır.",

        "footer_contact": "Xəta və təkliflər üçün",
    },
    "en": {
        "page_title": "Multi Tools (SteamID • QR • Images)",
        "lang_label": "Language",
        "tabs_titles": ["SteamID64 Finder", "QR Code Generator", "Photo Saver"],

        "steam_title": "🎮 SteamID Finder",
        "steam_caption": "Fetch details by profile link, vanity username, or SteamID64.",
        "steam_input": "Profile URL, Vanity Username, or SteamID64",
        "steam_ph": "e.g., https://steamcommunity.com/id/gaben | gaben | 7656...",
        "steam_btn": "Search",
        "steam_found": "Found!",
        "steam_warn_api": "⚠️ Please set `STEAM_API_KEY` as a secret/ENV.",
        "steam_display": "Display Name",
        "steam_username": "Username",
        "steam_sid64": "SteamID64",
        "steam_level": "Level",
        "copy": "Copy",
        "copied": "Copied!",
        "copy_failed": "Copy failed: ",

        "qr_title": "🔗 Create QR Code from URL",
        "qr_caption": "Generate a QR code for the URL you enter.",
        "qr_input": "URL",
        "qr_ph": "https://example.com",
        "qr_btn": "Generate QR",
        "qr_warn": "Please enter a URL first.",
        "qr_error": "An error occurred: ",
        "qr_download": "⤓ Download QR",
        "qr_preview": "🔍 Generated QR Code",

        "ps_title": "📥 Bulk Image Downloader",
        "ps_caption": "Paste links and download images as a ZIP.",
        "ps_area": "Paste image URLs, one per line:",
        "ps_btn": "Create ZIP",
        "ps_need": "Please enter at least one URL.",
        "ps_ready": "{} image(s) detected. ZIP is ready.",
        "ps_dl": "Download ZIP",
        "ps_errorlog": "error_log.txt",
        "footer_tip": "Icons below link to popular image services.",

        "footer_contact": "For bugs & feedback",
    },
    "pt_BR": {
        "page_title": "Multi Tools (SteamID • QR • Imagens)",
        "lang_label": "Idioma",
        "tabs_titles": ["Localizador de SteamID64", "Gerador de QR Code", "Salvador de Imagens"],

        "steam_title": "🎮 Localizador de SteamID",
        "steam_caption": "Obtenha detalhes pelo link do perfil, nome vanity ou SteamID64.",
        "steam_input": "URL do Perfil, Nome (vanity) ou SteamID64",
        "steam_ph": "ex.: https://steamcommunity.com/id/gaben | gaben | 7656...",
        "steam_btn": "Buscar",
        "steam_found": "Encontrado!",
        "steam_warn_api": "⚠️ Defina `STEAM_API_KEY` como segredo/variável de ambiente.",
        "steam_display": "Nome Exibido",
        "steam_username": "Nome de usuário",
        "steam_sid64": "SteamID64",
        "steam_level": "Nível",
        "copy": "Copiar",
        "copied": "Copiado!",
        "copy_failed": "Falha ao copiar: ",

        "qr_title": "🔗 Criar QR Code de URL",
        "qr_caption": "Gere um QR code para a URL informada.",
        "qr_input": "URL",
        "qr_ph": "https://example.com",
        "qr_btn": "Gerar QR",
        "qr_warn": "Insira uma URL primeiro.",
        "qr_error": "Ocorreu um erro: ",
        "qr_download": "⤓ Baixar QR",
        "qr_preview": "🔍 QR Code Gerado",

        "ps_title": "📥 Baixador de Imagens em Lote",
        "ps_caption": "Cole links e baixe imagens em um ZIP.",
        "ps_area": "Cole URLs de imagens, uma por linha:",
        "ps_btn": "Criar ZIP",
        "ps_need": "Insira pelo menos uma URL.",
        "ps_ready": "{} imagem(ns) detectada(s). ZIP pronto.",
        "ps_dl": "Baixar ZIP",
        "ps_errorlog": "error_log.txt",
        "footer_tip": "Ícones abaixo levam a serviços populares de imagens.",

        "footer_contact": "Para bugs e sugestões",
    },
    "es": {
        "page_title": "Multi Tools (SteamID • QR • Imágenes)",
        "lang_label": "Idioma",
        "tabs_titles": ["Buscador de SteamID64", "Generador de Código QR", "Guardador de Imágenes"],

        "steam_title": "🎮 Buscador de SteamID",
        "steam_caption": "Obtén detalles por enlace de perfil, nombre vanity o SteamID64.",
        "steam_input": "URL del Perfil, Nombre (vanity) o SteamID64",
        "steam_ph": "p. ej.: https://steamcommunity.com/id/gaben | gaben | 7656...",
        "steam_btn": "Buscar",
        "steam_found": "¡Encontrado!",
        "steam_warn_api": "⚠️ Configura `STEAM_API_KEY` como secreto/variable de entorno.",
        "steam_display": "Nombre Visible",
        "steam_username": "Nombre de usuario",
        "steam_sid64": "SteamID64",
        "steam_level": "Nivel",
        "copy": "Copiar",
        "copied": "¡Copiado!",
        "copy_failed": "Error al copiar: ",

        "qr_title": "🔗 Crear código QR desde URL",
        "qr_caption": "Genera un código QR para la URL ingresada.",
        "qr_input": "URL",
        "qr_ph": "https://example.com",
        "qr_btn": "Generar QR",
        "qr_warn": "Primero ingresa una URL.",
        "qr_error": "Ocurrió un error: ",
        "qr_download": "⤓ Descargar QR",
        "qr_preview": "🔍 Código QR Generado",

        "ps_title": "📥 Descargador Masivo de Imágenes",
        "ps_caption": "Pega enlaces y descarga las imágenes en un ZIP.",
        "ps_area": "Pega las URLs de imágenes, una por línea:",
        "ps_btn": "Crear ZIP",
        "ps_need": "Ingresa al menos una URL.",
        "ps_ready": "{} imagen(es) detectada(s). ZIP listo.",
        "ps_dl": "Descargar ZIP",
        "ps_errorlog": "error_log.txt",
        "footer_tip": "Los íconos abajo enlazan a servicios populares de imágenes.",

        "footer_contact": "Para errores y sugerencias",
    },
    "ru": {
        "page_title": "Multi Tools (SteamID • QR • Изображения)",
        "lang_label": "Язык",
        "tabs_titles": ["Поиск SteamID64", "Генератор QR-кодов", "Сохранение изображений"],

        "steam_title": "🎮 Поиск SteamID",
        "steam_caption": "Получите данные по ссылке профиля, имени (vanity) или SteamID64.",
        "steam_input": "URL профиля, Имя (vanity) или SteamID64",
        "steam_ph": "напр.: https://steamcommunity.com/id/gaben | gaben | 7656...",
        "steam_btn": "Найти",
        "steam_found": "Найдено!",
        "steam_warn_api": "⚠️ Укажите `STEAM_API_KEY` в переменных окружения.",
        "steam_display": "Отображаемое имя",
        "steam_username": "Имя пользователя",
        "steam_sid64": "SteamID64",
        "steam_level": "Уровень",
        "copy": "Копировать",
        "copied": "Скопировано!",
        "copy_failed": "Ошибка копирования: ",

        "qr_title": "🔗 Создать QR-код из URL",
        "qr_caption": "Сгенерируйте QR-код для введённого URL.",
        "qr_input": "URL",
        "qr_ph": "https://example.com",
        "qr_btn": "Создать QR",
        "qr_warn": "Сначала введите URL.",
        "qr_error": "Произошла ошибка: ",
        "qr_download": "⤓ Скачать QR",
        "qr_preview": "🔍 Сгенерированный QR-код",

        "ps_title": "📥 Массовая загрузка изображений",
        "ps_caption": "Вставьте ссылки и скачайте изображения в ZIP.",
        "ps_area": "Вставьте URL изображений, по одному в строке:",
        "ps_btn": "Создать ZIP",
        "ps_need": "Введите хотя бы один URL.",
        "ps_ready": "Обнаружено изображений: {}. ZIP готов.",
        "ps_dl": "Скачать ZIP",
        "ps_errorlog": "error_log.txt",
        "footer_tip": "Иконки ниже ведут на популярные сервисы изображений.",

        "footer_contact": "Для ошибок и предложений",
    },
}

LANG_FLAGS = {
    "tr": "🇹🇷 Türkçe",
    "az": "🇦🇿 Azərbaycan",
    "en": "🇬🇧 English",
    "pt_BR": "🇧🇷 Português (BR)",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
}

def T(key: str) -> str:
    lang = st.session_state.get("lang") or "tr"
    return I18N.get(lang, I18N["tr"]).get(key, key)

# ================== Dil Seçim Ekranı ==================
if "lang" not in st.session_state:
    st.session_state.lang = None

if st.session_state.lang is None:
    st.title("🌍 Select Your Language / Dil Seçin")
    st.markdown("### Devam etmek için bir dil seçiniz 👇")

    cols = st.columns(3)
    i = 0
    for code, label in LANG_FLAGS.items():
        with cols[i % 3]:
            if st.button(label, key=f"lang_{code}", use_container_width=True):
                st.session_state.lang = code
                st.rerun()
        i += 1
    st.stop()

# ================== Üstte Dil Değiştirici (opsiyonel) ==================
with st.sidebar:
    new_lang = st.selectbox("🌐 Language / Dil", list(LANG_FLAGS.keys()),
                            index=list(LANG_FLAGS.keys()).index(st.session_state.lang),
                            format_func=lambda x: LANG_FLAGS[x])
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

# ================== Ortak Utils ==================
def html_escape(s: str) -> str:
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def _js_json(s: str) -> str:
    return json.dumps(s if s is not None else "")

# ================== Steam Finder Helpers ==================
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
CDN_PREFIX = "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/"
STEAMID64_RE    = re.compile(r"^(7656\d{13})$")
URL_PROFILES_RE = re.compile(r"https?://steamcommunity\.com/profiles/(7656\d{13})(?:/.*)?", re.I)
URL_ID_RE       = re.compile(r"https?://steamcommunity\.com/id/([A-Za-z0-9\-_.]+)(?:/.*)?", re.I)

def _fix(url):
    if isinstance(url, str) and url.startswith("items/"):
        return CDN_PREFIX + url
    return url if isinstance(url, str) else None

def resolve_vanity(vanity, key):
    if not key:
        raise ValueError("STEAM_API_KEY required to resolve vanity.")
    r = requests.get(
        "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/",
        params={"key": key, "vanityurl": vanity},
        timeout=10,
    )
    r.raise_for_status()
    d = r.json().get("response", {})
    if d.get("success") != 1:
        raise ValueError(f"Vanity could not be resolved: {d.get('message','unknown')}")
    return d["steamid"]

def resolve_input_to_steamid64(text, key):
    s = text.strip()
    if not s: raise ValueError("Empty input.")
    if m := URL_PROFILES_RE.match(s): return m.group(1)
    if m := URL_ID_RE.match(s):       return resolve_vanity(m.group(1), key)
    if STEAMID64_RE.match(s):         return s
    if re.fullmatch(r"[A-Za-z0-9\-_.]+", s): return resolve_vanity(s, key)
    raise ValueError("Invalid input. Expecting profile URL, steamid64 or vanity.")

@st.cache_data(ttl=300, show_spinner=False)
def get_player(steamid64, key):
    r = requests.get(
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
        params={"key": key, "steamids": steamid64},
        timeout=10,
    )
    r.raise_for_status()
    players = r.json().get("response", {}).get("players", [])
    return players[0] if players else None

@st.cache_data(ttl=300, show_spinner=False)
def get_level(steamid64, key):
    r = requests.get(
        "https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/",
        params={"key": key, "steamid": steamid64},
        timeout=10,
    )
    if r.status_code != 200: return None
    return r.json().get("response", {}).get("player_level")

@st.cache_data(ttl=300, show_spinner=False)
def get_items(steamid64, key):
    r = requests.get(
        "https://api.steampowered.com/IPlayerService/GetProfileItemsEquipped/v1/",
        params={"key": key, "steamid": steamid64},
        timeout=10,
    )
    if r.status_code != 200: return None
    data = r.json().get("response", {}) or {}
    for sec in ("avatar_frame", "animated_avatar"):
        val = data.get(sec)
        if isinstance(val, dict):
            fixed = {k: _fix(v) for k, v in val.items()}
            data[sec] = fixed
    return data

def choose_avatar(player, items):
    anim = (items or {}).get("animated_avatar") or {}
    for k in ("image_large","image_small","image"):
        u = anim.get(k)
        if isinstance(u, str) and u:
            if u.endswith((".webm",".mp4")): return u, True
            return u, False
    if player and isinstance(player.get("avatarfull"), str):
        return player["avatarfull"], False
    return None, False

def choose_frame(items):
    f = (items or {}).get("avatar_frame") or {}
    for k in ("image_large","image_small","image"):
        u = f.get(k)
        if isinstance(u, str) and u: return u
    return None

def guess_vanity(input_text: str, player: dict | None) -> str | None:
    s = (input_text or "").strip()
    if m := URL_ID_RE.match(s): return m.group(1)
    if s and not URL_PROFILES_RE.match(s) and not STEAMID64_RE.match(s) and re.fullmatch(r"[A-Za-z0-9\-_.]+", s):
        return s
    prof = (player or {}).get("profileurl")
    if isinstance(prof, str):
        m = URL_ID_RE.match(prof)
        if m: return m.group(1)
    return None

def copy_row(label: str, value: str, copyable: bool, key: str):
    """HTML/JS içinde { } kaçışlarını düzelten, f-stringsiz güvenli versiyon."""
    js_text = json.dumps(value if value else "")
    html_text = html_escape(value if value else "—")
    copy_title = json.dumps(T("copy"))
    copied_msg = json.dumps(T("copied"))
    copy_failed_msg = json.dumps(T("copy_failed"))

    button_html = (
        """
        <button class='copy-btn' title={copy_title} aria-label={copy_title}>
          <svg viewBox='0 0 24 24'>
            <path d='M16 1H4c-1.1 0-2 .9-2 2v12h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14
            c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z'/>
          </svg>
        </button>
        """.format(copy_title=copy_title)
        if copyable else ""
    )

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  :root {{
    --code-bg: rgba(127,127,127,.12);
    --code-border: rgba(127,127,127,.3);
  }}
  html, body {{ margin:0; padding:0; background:transparent; }}
  .row {{ display:flex; align-items:center; justify-content:center; gap:12px; flex-wrap:wrap;
          font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
  .label {{ font-weight:700; min-width:190px; text-align:right; }}
  .code  {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            padding:7px 10px; border-radius:6px; background:var(--code-bg); border:1px solid var(--code-border); }}
  .copy-btn {{ border:none; background:transparent; cursor:pointer; display:inline-flex; align-items:center; margin-left:6px; }}
  .copy-btn svg {{ width:18px; height:18px; fill: currentColor; opacity:.9; }}
  .copy-btn:hover {{ transform: scale(1.1); }}
</style>
</head>
<body>
  <div class="row" id="row">
    <span class="label">{label}:</span>
    <code class="code">{html_text}</code>
    {button_html}
  </div>

<script>
(function() {{
  try {{
    const app = window.parent.document.querySelector('.stApp');
    const root = window.parent.getComputedStyle(app);
    const textColor = root.color || '#222';
    const bg2 = root.getPropertyValue('--secondary-background-color') || '';
    const divider = root.getPropertyValue('--divider-color') || '';
    document.body.style.color = textColor;
    if (bg2) document.documentElement.style.setProperty('--code-bg', bg2.trim());
    if (divider) document.documentElement.style.setProperty('--code-border', divider.trim());
  }} catch (e) {{
    document.body.style.color = '#222';
  }}

  const btn = document.querySelector('button.copy-btn');
  if (btn) {{
    btn.addEventListener('click', async () => {{
      try {{
        await navigator.clipboard.writeText({js_text});
        btn.title = {copied_msg};
      }} catch (e) {{
        alert({copy_failed_msg} + e);
      }}
    }});
  }}
}})();
</script>
</body>
</html>
    """.format(
        label=label,
        html_text=html_text,
        button_html=button_html,
        js_text=js_text,
        copied_msg=copied_msg,
        copy_failed_msg=copy_failed_msg,
    )

    components.html(html, height=50, scrolling=False)

# ================== Photo Saver Helpers ==================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    )
}
IMG_EXTS = (".jpg",".jpeg",".png",".gif",".webp",".bmp")

def resolve_image_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lstrip("/")
    base, ext = os.path.splitext(path)

    # imgur page → og:image
    if "imgur.com" in host and not host.startswith("i.imgur.com"):
        try:
            resp = scraper.get(url, headers={**HEADERS, "Referer": url}, timeout=10)
            resp.raise_for_status()
            if HAVE_SCRAPER:
                soup = BeautifulSoup(resp.text, "lxml")
                m = soup.find("meta", property="og:image")
                if m and m.get("content"):
                    img = m["content"]
                    return img if img.startswith("http") else "https:" + img
        except Exception:
            pass

    # i.imgur.com raw
    if host.startswith("i.imgur.com"):
        if ext.lower() in IMG_EXTS:
            return url
        for e in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
            cand = url + e
            try:
                h = scraper.head(cand, headers={**HEADERS, "Referer": url}, timeout=5)
                ctype = getattr(h, "headers", {}).get("Content-Type","")
                if getattr(h, "status_code", None) == 200 and str(ctype).startswith("image/"):
                    return cand
            except Exception:
                continue
        return url + ".jpg"

    # already has extension
    if ext.lower() in IMG_EXTS:
        return url

    # generic meta fallbacks
    try:
        resp = scraper.get(url, headers={**HEADERS, "Referer": url}, timeout=10)
        resp.raise_for_status()
        if HAVE_SCRAPER:
            soup = BeautifulSoup(resp.text, "lxml")
            for key, attr in (("property","og:image"), ("name","twitter:image")):
                m = soup.find("meta", **{key:attr})
                if m and m.get("content"):
                    img = m["content"]
                    return img if img.startswith("http") else "https:" + img
    except Exception:
        pass

    return url

def download_images_and_zip(urls: list[str]) -> bytes:
    buf = io.BytesIO()
    error_log_name = T("ps_errorlog")
    with zipfile.ZipFile(buf, "w") as z:
        for i, url in enumerate(urls, start=1):
            real = resolve_image_url(url)
            parsed = urlparse(real)
            name = os.path.basename(parsed.path) or f"image_{i}.jpg"
            try:
                r = scraper.get(real, headers={**HEADERS, "Referer": url}, timeout=15)
                r.raise_for_status()
                z.writestr(name, r.content)
            except Exception as e:
                err = f"{url} → {e}\n"
                if error_log_name not in z.namelist():
                    z.writestr(error_log_name, err)
                else:
                    existing = z.read(error_log_name).decode(errors="ignore")
                    z.writestr(error_log_name, existing + err)
    return buf.getvalue()

# ================== UI ==================
st.title("🧰 Multi Tools")
st.caption("SteamID Finder • QR Code • Photo Saver")

tab1, tab2, tab3 = st.tabs(I18N[st.session_state.lang]["tabs_titles"])

# ---------- TAB 1: SteamID Finder ----------
with tab1:
    st.header(T("steam_title"))
    st.caption(T("steam_caption"))
    if not STEAM_API_KEY:
        st.warning(T("steam_warn_api"))

    st.markdown("""
<style>
.stApp{ text-align:center; }
input, .stButton>button{ margin:0 auto; display:block; }
.avatar-box{ position:relative; width:160px; height:160px; overflow:hidden; border-radius:12px; margin:16px auto; }
.avatar-box img,.avatar-box video{ width:160px; height:160px; object-fit:cover; border-radius:12px; }
.avatar-box .frame{ position:absolute; top:0; left:0; width:160px; height:160px; pointer-events:none; }
.level{ display:inline-flex; align-items:center; gap:8px; border-radius:999px; padding:6px 12px; font-weight:600;
        border:1px solid var(--divider-color, rgba(127,127,127,.35));
        background: var(--secondary-background-color, rgba(127,127,127,.12)); }
.level-dot{ width:12px; height:12px; border-radius:50%; background:#ff4d4f; }
</style>
""", unsafe_allow_html=True)

    s_inp = st.text_input(T("steam_input"), placeholder=T("steam_ph"))
    if st.button(T("steam_btn")) and s_inp.strip():
        try:
            sid64 = resolve_input_to_steamid64(s_inp, STEAM_API_KEY)
            st.success(T("steam_found"))

            player = get_player(sid64, STEAM_API_KEY)
            level  = get_level(sid64, STEAM_API_KEY)
            items  = get_items(sid64, STEAM_API_KEY)

            personaname = (player or {}).get("personaname", "—")
            vanity      = guess_vanity(s_inp, player) or "—"

            avatar_u, is_video = choose_avatar(player, items)
            frame_u  = choose_frame(items)

            # avatar kutusu
            html_parts = ['<div class="avatar-box">']
            if avatar_u:
                if is_video:
                    html_parts.append('<video src="{0}" autoplay muted loop playsinline></video>'.format(avatar_u))
                else:
                    html_parts.append('<img src="{0}" alt="avatar">'.format(avatar_u))
            else:
                html_parts.append('<div style="width:160px;height:160px;"></div>')
            if frame_u:
                html_parts.append('<img class="frame" src="{0}" alt="frame">'.format(frame_u))
            html_parts.append('</div>')
            st.markdown("".join(html_parts), unsafe_allow_html=True)

            level_val = level if isinstance(level, int) else "—"
            st.markdown(
                "<div class='level'><span class='level-dot'></span>{} {}</div>".format(T("steam_level"), level_val),
                unsafe_allow_html=True
            )

            copy_row(T("steam_display"), personaname, False, "display_name")
            copy_row(T("steam_username"), vanity, True, "vanity")
            copy_row(T("steam_sid64"), sid64, True, "sid64")

        except Exception as e:
            st.error(str(e))

# ---------- TAB 2: QR Code ----------
with tab2:
    st.header(T("qr_title"))
    st.caption(T("qr_caption"))

    url = st.text_input(T("qr_input"), placeholder=T("qr_ph"))
    if st.button(T("qr_btn")):
        if not url:
            st.warning(T("qr_warn"))
        else:
            try:
                qr_api = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={}".format(url)
                resp = requests.get(qr_api, timeout=15)
                resp.raise_for_status()
                img_bytes = resp.content
                if HAVE_PIL:
                    img = Image.open(BytesIO(img_bytes))
                    st.image(img, caption=T("qr_preview"), use_container_width=True)
                else:
                    st.image(img_bytes, caption=T("qr_preview"), use_container_width=True)
                st.download_button(
                    label=T("qr_download"),
                    data=img_bytes,
                    file_name="qr.png",
                    mime="image/png",
                )
            except Exception as e:
                st.error(T("qr_error") + str(e))

# ---------- TAB 3: Photo Saver ----------
with tab3:
    st.header(T("ps_title"))
    st.caption(T("ps_caption"))

    urls_input = st.text_area(T("ps_area"), height=200,
                              placeholder="https://i.imgur.com/xxxx\nhttps://example.com/page-with-image")
    urls = [u.strip() for u in urls_input.splitlines() if u.strip()]

    if st.button(T("ps_btn")):
        if not urls:
            st.error(T("ps_need"))
        else:
            zip_bytes = download_images_and_zip(urls)
            today = datetime.now().strftime("%d.%m.%Y")
            filename = "{}.zip".format(today)
            st.success(T("ps_ready").format(len(urls)))
            st.download_button(
                label=T("ps_dl"),
                data=zip_bytes,
                file_name=filename,
                mime="application/zip"
            )

    st.divider()
    st.caption(T("footer_tip"))
    logos = [
        ("https://st.prntscr.com/2023/07/24/0635/img/icon_lightshot.png", "https://prnt.sc/"),
        ("https://simgbb.com/images/logo.png", "https://imgbb.com/"),
        ("https://e7.pngegg.com/pngimages/155/2/png-clipart-imgur-android-android-text-logo-thumbnail.png", "https://imgur.com/upload"),
    ]
    cols = st.columns(len(logos))
    for i, (logo, link) in enumerate(logos):
        with cols[i]:
            st.markdown("<a href='{0}' target='_blank'><img src='{1}' alt='logo' height='40'/></a>".format(link, logo),
                        unsafe_allow_html=True)

# ---------- Footer (global) ----------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; opacity:.9'>{}: <a href='mailto:info@sinankeskin.com.tr'>info@sinankeskin.com.tr</a></div>"
    .format(T("footer_contact")),
    unsafe_allow_html=True
)
