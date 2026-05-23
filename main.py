import streamlit as st
import requests
import json
import random
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz

st.set_page_config(
    page_title="NEURO-AGRO // Cyber Irrigation",
    page_icon="⚡",
    layout="wide"
)

# ============================================================
# KONFIGURASI
# ============================================================
FIREBASE_URL = "https://agritech-bantul-default-rtdb.firebaseio.com/"

# ============================================================
# CSS RESPONSIF (LAPTOP + HP iOS/ANDROID)
# ============================================================
st.markdown("""
<style>/* ===================================================================== */
    /* TAMBAHAN RACIKAN CYBER-AGRITECH (ANIMASI LOGO & BACKGROUND BERGERAK) */
    /* ===================================================================== */
    
    /* 1. Background Animasi Bergerak Tema Cyberpunk-Agritech */
    .stApp {
        background: radial-gradient(circle at center, #0a1f12 0%, #020804 100%) !important;
        background-size: 400% 400% !important;
        animation: cyberWave 15s ease infinite !important;
    }
    
    @keyframes cyberWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Efek Network Cyberpunk: Node sensor + koneksi garis tebal */
    .stApp::before {
        content: "";
        position: absolute;
        inset: 0;
        background-color: #020804;
        background-image:
            radial-gradient(circle at 14% 18%, rgba(0, 255, 128, 0.95) 4px, transparent 8px),
            radial-gradient(circle at 34% 52%, rgba(0, 255, 128, 0.76) 3.2px, transparent 7px),
            radial-gradient(circle at 58% 22%, rgba(0, 255, 128, 0.9) 5px, transparent 9px),
            radial-gradient(circle at 80% 68%, rgba(0, 255, 128, 0.82) 3.5px, transparent 7px),
            linear-gradient(120deg, rgba(0, 255, 128, 0.45) 2.5px, transparent 2.5px),
            linear-gradient(25deg, rgba(0, 255, 128, 0.34) 2.2px, transparent 2.2px),
            linear-gradient(70deg, rgba(0, 255, 128, 0.20) 2px, transparent 2px);
        background-size: 240px 240px, 200px 200px, 220px 220px, 260px 260px, 160px 160px, 180px 180px, 220px 220px;
        background-blend-mode: screen;
        filter: drop-shadow(0 0 18px rgba(0, 255, 128, 0.35));
        pointer-events: none;
        z-index: 0;
        opacity: 0.98;
        animation: networkFlow 20s linear infinite;
    }

    .stApp::after {
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(circle at 12% 22%, rgba(0,255,128,0.42) 3.5px, transparent 6px),
            radial-gradient(circle at 42% 60%, rgba(0,255,128,0.36) 2.8px, transparent 6px),
            radial-gradient(circle at 70% 42%, rgba(0,255,128,0.52) 4.2px, transparent 8px),
            radial-gradient(circle at 88% 78%, rgba(0,255,128,0.30) 3px, transparent 6px),
            linear-gradient(145deg, rgba(0, 255, 128, 0.55) 2.5px, transparent 2.5px),
            linear-gradient(55deg, rgba(0, 255, 128, 0.32) 2px, transparent 2px);
        background-size: 120% 120%, 120% 120%, 120% 120%, 120% 120%, 200px 200px, 180px 180px;
        mix-blend-mode: screen;
        filter: blur(0.6px);
        opacity: 0.76;
        pointer-events: none;
        z-index: 0;
        animation: networkPulse 16s ease-in-out infinite alternate;
    }

    @keyframes networkFlow {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-28px, 24px) scale(1.01); }
        100% { transform: translate(-56px, 48px) scale(1); }
    }

    @keyframes networkPulse {
        0% { opacity: 0.65; }
        50% { opacity: 0.86; }
        100% { opacity: 0.70; }
    }

    /* 2. Animasi Logo AI: Menyala Neon (Pulse) tanpa rotasi, tetap diam namun hidup */
    [data-testid="stAppViewBlockContainer"] img, .stImage img, img, .animated-logo svg {
        filter: drop-shadow(0 0 10px rgba(0, 255, 128, 1)) !important;
        animation: aiPulse 2.5s ease-in-out infinite alternate !important;
    }

    .animated-logo svg {
        transform-style: preserve-3d;
        filter: drop-shadow(0 0 12px rgba(0, 255, 128, 1)) drop-shadow(0 0 28px rgba(0, 255, 128, 0.55));
    }

    .animated-logo svg .leaf-left,
    .animated-logo svg .leaf-right {
        transform-origin: 45px 48px;
    }

    .animated-logo svg .leaf-left {
        animation: leafSwingLeft 5s ease-in-out infinite alternate;
    }

    .animated-logo svg .leaf-right {
        animation: leafSwingRight 5s ease-in-out infinite alternate;
    }

    @keyframes aiPulse {
        0% {
            opacity: 0.88;
            filter: drop-shadow(0 0 5px rgba(0, 255, 128, 0.45));
        }
        50% {
            opacity: 1;
            filter: drop-shadow(0 0 18px rgba(0, 255, 128, 1)) drop-shadow(0 0 34px rgba(0, 255, 128, 0.55));
        }
        100% {
            opacity: 0.92;
            filter: drop-shadow(0 0 6px rgba(0, 255, 128, 0.55));
        }
    }

    @keyframes leafSwingLeft {
        0% { transform: translateX(0) rotate(0deg); }
        100% { transform: translateX(-2px) rotate(-3deg); }
    }

    @keyframes leafSwingRight {
        0% { transform: translateX(0) rotate(0deg); }
        100% { transform: translateX(2px) rotate(3deg); }
    }

    /* Efek Glow Tambahan pada Tulisan Judul */
    h1, h2, h3 {
        text-shadow: 0 0 10px rgba(0, 255, 128, 0.4) !important;
    }
    /* === GLOBAL === */
    .block-container {
        padding-top: 6rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1200px !important;
    }

    /* === HEADER BRANDING === */
    .brand-title {
        font-family: 'Courier New', Courier, monospace;
        font-weight: 900;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .brand-sub {
        font-size: 13px;
        font-style: italic;
        color: #888888;
        text-align: center;
        letter-spacing: 2px;
        margin-top: 4px;
    }
    .brand-credit {
        font-size: 11px;
        font-weight: bold;
        color: #00E676;
        text-align: center;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: -4px;
    }
    .waktu-box {
        text-align: center;
        color: #888;
        font-size: 13px;
        padding: 4px 0 8px 0;
    }

    /* === METRIC CARDS === */
    [data-testid="stMetric"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 12px 16px !important;
        margin-bottom: 8px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    /* === TOMBOL === */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 10px 16px !important;
        width: 100% !important;
        min-height: 48px !important;
    }

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        min-width: 220px !important;
        max-width: 260px !important;
    }

    /* === MOBILE (layar ≤ 768px) === */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        .brand-title {
            font-size: 18px !important;
            letter-spacing: 1px !important;
        }
        .brand-sub {
            font-size: 11px !important;
            letter-spacing: 1px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 18px !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 11px !important;
        }
        .stButton > button {
            font-size: 13px !important;
            min-height: 44px !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            font-size: 12px !important;
            padding: 8px 12px !important;
        }
        /* Kolom Streamlit wrap ke bawah di HP */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            min-width: 45% !important;
            flex: 1 1 45% !important;
        }
    }

    /* === MOBILE KECIL (layar ≤ 480px) === */
    @media (max-width: 480px) {
        .brand-title {
            font-size: 15px !important;
            letter-spacing: 0px !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER BRANDING + JAM LIVE WIB
# ============================================================
zona_wib = pytz.timezone("Asia/Jakarta")
waktu_sekarang = datetime.now(zona_wib)

hari_indo = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

nama_hari = hari_indo[waktu_sekarang.weekday()]
nama_bulan = bulan_indo[waktu_sekarang.month - 1]
format_waktu = waktu_sekarang.strftime(f"{nama_hari}, %d {nama_bulan} %Y | 🕒 %H:%M WIB")

st.markdown(f"""
<style>
  .header-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    padding: 8px 0 4px 0;
    flex-wrap: wrap;
  }}
  .logo-svg {{
    flex-shrink: 0;
  }}
  .header-text {{
    text-align: left;
  }}
  @media (max-width: 600px) {{
    .header-wrap {{
      flex-direction: column;
      gap: 8px;
    }}
    .header-text {{
      text-align: center;
    }}
    .logo-svg svg {{
      width: 64px !important;
      height: 64px !important;
    }}
  }}
</style>

<div class="header-wrap">
  <!-- LOGO SVG -->
  <div class="logo-svg animated-logo">
    <svg width="90" height="90" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer hexagon ring -->
      <polygon points="45,4 82,24 82,66 45,86 8,66 8,24"
               stroke="#00E676" stroke-width="2" fill="#0a1a0f"/>
      <!-- Inner hex -->
      <polygon points="45,14 74,30 74,60 45,76 16,60 16,30"
               stroke="#00E676" stroke-width="1" fill="#0d2218" stroke-dasharray="4,2"/>
      <!-- Circuit lines horizontal -->
      <line x1="16" y1="45" x2="30" y2="45" stroke="#00E676" stroke-width="1.5"/>
      <line x1="60" y1="45" x2="74" y2="45" stroke="#00E676" stroke-width="1.5"/>
      <!-- Circuit dots -->
      <circle cx="30" cy="45" r="2.5" fill="#00E676"/>
      <circle cx="60" cy="45" r="2.5" fill="#00E676"/>
      <!-- Stem -->
      <line x1="45" y1="62" x2="45" y2="48" stroke="#00E676" stroke-width="2" stroke-linecap="round"/>
      <!-- Left leaf -->
      <path class="leaf-left" d="M45 55 Q34 46 34 36 Q42 40 45 48" fill="#00E676" opacity="0.85"/>
      <!-- Right leaf -->
      <path class="leaf-right" d="M45 52 Q56 43 58 33 Q49 38 45 48" fill="#00C853" opacity="0.85"/>
      <!-- Top bud -->
      <circle cx="45" cy="32" r="4" fill="#00E676" opacity="0.6"/>
      <circle cx="45" cy="32" r="2" fill="#00E676"/>
      <!-- Corner dots -->
      <circle cx="8"  cy="45" r="2" fill="#00E676" opacity="0.5"/>
      <circle cx="82" cy="45" r="2" fill="#00E676" opacity="0.5"/>
      <!-- Pulse ring animation -->
      <circle cx="45" cy="45" r="36" stroke="#00E676" stroke-width="0.5"
              fill="none" opacity="0.25" stroke-dasharray="3,5"/>
    </svg>
  </div>

  <!-- TEKS JUDUL -->
  <div class="header-text">
    <p style="font-family:'Courier New',Courier,monospace; font-weight:900;
               font-size:clamp(16px,2.5vw,28px); letter-spacing:2px;
               margin:0; line-height:1.2; color:#f0f0f0;">
      ⚡ NEURO-AGRO <span style="color:#00E676;">// CYBER IRRIGATION</span> 🛰️
    </p>
    <p style="font-size:clamp(10px,1.2vw,13px); font-style:italic;
               color:#888888; letter-spacing:2px; margin:4px 0 2px 0;">
      Next-Gen Autonomous AI Core Ecosystem &bull; Bantul Region
    </p>
    <p style="font-size:11px; font-weight:bold; color:#00E676;
               letter-spacing:4px; text-transform:uppercase; margin:0;">
      by m.zaky
    </p>
  </div>
</div>

<p style="text-align:center; color:#888; font-size:13px; margin:6px 0 0 0;">
  📅 {format_waktu}
</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# SIDEBAR — SIMULASI & INFO
# ============================================================
st.sidebar.title("🎛️ Panel Simulasi")
st.sidebar.markdown("Gunakan tombol di bawah untuk menguji respons AI saat hardware belum terpasang.")

if st.sidebar.button("Simulasi: Siram Lahan 💧"):
    st.session_state.kelembapan_tanah = random.randint(70, 85)
    st.session_state.temperatur_tanah = 24
    st.session_state.mode = "Simulasi 🔵"

if st.sidebar.button("Simulasi: Lahan Kering ☀️"):
    st.session_state.kelembapan_tanah = random.randint(30, 40)
    st.session_state.temperatur_tanah = 29
    st.session_state.mode = "Simulasi 🔵"

if st.sidebar.button("🎲 Generate Data Sensor Acak"):
    st.session_state.kelembapan_tanah = random.randint(30, 75)
    st.session_state.temperatur_tanah = round(random.uniform(24.0, 32.0), 1)
    st.session_state.mode = "Simulasi 🔵"

st.sidebar.markdown("---")
st.sidebar.info("Saat hardware ESP32 sudah terpasang, data sensor akan diambil otomatis dari Firebase.")

# ============================================================
# 1. DATA CUACA REAL-TIME (Open-Meteo API)
# ============================================================
st.markdown("### 🌤️ Data Cuaca Real-Time (Satelit Open-Meteo — Bantul)")

@st.cache_data(ttl=600)
def ambil_data_cuaca_realtime():
    try:
        latitude = "-7.8953"
        longitude = "110.3347"
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,rain,weather_code"
            f"&timezone=Asia%2FJakarta"
        )
        response = requests.get(url, timeout=5).json()
        current = response["current"]

        suhu_asli = current["temperature_2m"]
        kelembapan_udara_asli = current["relative_humidity_2m"]
        hujan_asli = current.get("rain", 0)
        code = current["weather_code"]

        if code == 0:
            cuaca_txt = "Cerah"
        elif code in [1, 2, 3]:
            cuaca_txt = "Cerah Berawan"
        elif code in [45, 48]:
            cuaca_txt = "Berkabut"
        elif code in [51, 53, 55, 61, 63, 65]:
            cuaca_txt = "Gerimis/Hujan Ringan"
        elif code in [71, 73, 75, 77, 80, 81, 82, 95, 96, 99]:
            cuaca_txt = "Hujan Lebat"
        else:
            cuaca_txt = "Cerah Berawan"

        return suhu_asli, kelembapan_udara_asli, hujan_asli, cuaca_txt
    except Exception:
        return 29.5, 75, 0, "Cerah Berawan"

suhu_udara, kelembapan_udara, hujan, prediksi_cuaca = ambil_data_cuaca_realtime()

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Suhu Udara", f"{suhu_udara} °C")
col2.metric("☁️ Kelembapan Udara", f"{kelembapan_udara} %")
col3.metric("🌧️ Curah Hujan", f"{hujan} mm")
col4.metric("🌈 Kondisi Cuaca Bantul", prediksi_cuaca)

st.markdown("---")

# ============================================================
# 2. DATA SENSOR HARDWARE (Firebase / Simulasi)
# ============================================================
st.markdown("### 📡 Data Sensor Hardware (ESP32/Arduino)")

if "kelembapan_tanah" not in st.session_state:
    st.session_state.kelembapan_tanah = 48
    st.session_state.temperatur_tanah = 26
    st.session_state.pompa_status = "MATI 🛑"
    st.session_state.mode = "Simulasi 🔵"
    st.session_state.historis = []
    st.session_state.log_pompa = []
    st.session_state.log_ai = []

kelembapan_tanah = st.session_state.kelembapan_tanah
temperatur_tanah = st.session_state.temperatur_tanah

# Estimasi suhu tanah berbasis data riil suhu udara (standar: suhu udara - 2°C)
temperatur_tanah_estimasi = round(suhu_udara - 2.0, 1)

# Coba ambil dari Firebase
try:
    r = requests.get(f"{FIREBASE_URL}/sensor_data.json", timeout=3)
    data_hw = r.json()
    if data_hw and isinstance(data_hw, dict):
        fb_kelem = data_hw.get("kelembapan_tanah")
        fb_suhu  = data_hw.get("suhu_udara")
        if isinstance(fb_kelem, (int, float)):
            kelembapan_tanah = float(fb_kelem)
        if isinstance(fb_suhu, (int, float)):
            temperatur_tanah = float(fb_suhu)
        st.session_state.kelembapan_tanah = kelembapan_tanah
        st.session_state.temperatur_tanah = temperatur_tanah
        st.session_state.mode = "Firebase ✅"
except Exception:
    pass

# Rekam data historis (maks 30 titik)
if "historis" not in st.session_state:
    st.session_state.historis = []
st.session_state.historis.append({
    "Waktu": datetime.now().strftime("%H:%M:%S"),
    "Kelembapan Tanah (%)": float(kelembapan_tanah),
    "Suhu Tanah (°C)": float(temperatur_tanah),
    "Suhu Udara (°C)": float(suhu_udara),
})
if len(st.session_state.historis) > 30:
    st.session_state.historis = st.session_state.historis[-30:]

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.metric("💧 Kelembapan Tanah", f"{kelembapan_tanah} %")
    if kelembapan_tanah < 40:
        st.error("⚠️ Tanah Terlalu Kering!")
    elif kelembapan_tanah > 70:
        st.warning("⚠️ Tanah Terlalu Basah!")
    else:
        st.success("✅ Kelembapan Ideal")

with col_s2:
    st.metric("🪵 Temperatur Tanah (Estimasi AI)", f"{temperatur_tanah_estimasi} °C")

with col_s3:
    st.metric("⚡ Status Pompa", st.session_state.pompa_status)
    st.caption(f"Sumber data: **{st.session_state.mode}**")

st.markdown("---")

# ============================================================
# ALERT OTOMATIS — KONDISI KRITIS
# ============================================================
if kelembapan_tanah < 40:
    st.error(
        f"🚨 **ALERT KRITIS!** Kelembapan tanah sangat rendah: **{kelembapan_tanah}%** "
        f"— Segera nyalakan pompa atau periksa sensor!"
    )
    st.toast(f"⚠️ Kelembapan tanah kritis: {kelembapan_tanah}%!", icon="🚨")
elif kelembapan_tanah > 70:
    st.warning(
        f"⚠️ **ALERT:** Kelembapan tanah terlalu tinggi: **{kelembapan_tanah}%** "
        f"— Matikan pompa, periksa drainase lahan!"
    )
    st.toast(f"⚠️ Kelembapan tanah terlalu basah: {kelembapan_tanah}%!", icon="💦")

if suhu_udara > 34:
    st.warning(
        f"🌡️ **ALERT:** Suhu udara sangat tinggi: **{suhu_udara}°C** "
        f"— Risiko penguapan ekstrem, pantau kelembapan tanah lebih sering."
    )
    st.toast(f"🌡️ Suhu udara ekstrem: {suhu_udara}°C!", icon="🔥")

st.markdown("---")

# ============================================================
# 3. AI ENGINE (KEPUTUSAN OTOMATIS)
# ============================================================
st.markdown("### 🧠 AI Engine — Analisis & Rekomendasi Otomatis")

def analisa_keputusan_ai(suhu, kelem_udara, temp_tanah_est, cuaca, hujan_mm):
    # Kondisi 1: Hujan terdeteksi
    if "Hujan" in cuaca or hujan_mm > 2:
        aksi = "TUTUP SALURAN AIR 🛑"
        alasan = (
            f"Satelit mendeteksi wilayah Bantul sedang **{cuaca}**. "
            f"AI otomatis menutup saluran air untuk menghemat pasokan dan memanfaatkan air hujan alami."
        )
        level = "info"
    # Kondisi 2: Udara gersang + suhu panas (penguapan ekstrem)
    elif kelem_udara < 65 and suhu > 31:
        aksi = "BUKA SALURAN AIR 💧"
        alasan = (
            f"Kondisi Bantul sedang terik ({suhu}°C) dengan kelembapan udara rendah ({kelem_udara}%). "
            f"Udara kering memicu penguapan tinggi. AI membuka saluran air untuk menjaga kesegaran lahan."
        )
        level = "success"
    # Kondisi 3: Estimasi temperatur tanah terlalu panas
    elif temp_tanah_est > 30.0:
        aksi = "BUKA SALURAN AIR (Pendinginan Lahan) 💧"
        alasan = (
            f"Meskipun cuaca normal, estimasi temperatur tanah mencapai **{temp_tanah_est}°C** "
            f"(terlalu panas untuk mikroba). AI membuka air sejenak untuk mendinginkan area perakaran."
        )
        level = "success"
    # Kondisi 4: Semua stabil
    else:
        aksi = "TUTUP SALURAN AIR 🛑"
        alasan = (
            f"Tingkat kelembapan udara ({kelem_udara}%) dan estimasi temperatur tanah ({temp_tanah_est}°C) "
            f"saat ini dalam batas normal. Cuaca Bantul terpantau **{cuaca}**, penyiraman belum diperlukan."
        )
        level = "info"
    return aksi, alasan, level

keputusan_ai, alasan_ai, level_ai = analisa_keputusan_ai(
    suhu_udara, kelembapan_udara, temperatur_tanah_estimasi, prediksi_cuaca, hujan
)

if level_ai == "success":
    st.success(f"## 🔔 KEPUTUSAN AI: {keputusan_ai}")
elif level_ai == "warning":
    st.warning(f"## 🔔 KEPUTUSAN AI: {keputusan_ai}")
else:
    st.info(f"## 🔔 KEPUTUSAN AI: {keputusan_ai}")

st.info(f"**📋 Analisis Pertimbangan AI:** {alasan_ai}")

if "log_keputusan_ai" not in st.session_state:
    st.session_state.log_keputusan_ai = []

if not st.session_state.log_keputusan_ai or st.session_state.log_keputusan_ai[-1]["aksi"] != keputusan_ai:
    st.session_state.log_keputusan_ai.append({
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aksi": keputusan_ai,
        "cuaca": prediksi_cuaca,
        "kelembapan_udara": f"{kelembapan_udara} %",
        "suhu_tanah_estimasi": f"{temperatur_tanah_estimasi} °C"
    })
    if len(st.session_state.log_keputusan_ai) > 30:
        st.session_state.log_keputusan_ai = st.session_state.log_keputusan_ai[-30:]

with st.expander("📜 Riwayat & Log Keputusan Otomatis AI", expanded=True):
    if st.session_state.log_keputusan_ai:
        df_log_ai = pd.DataFrame(st.session_state.log_keputusan_ai).rename(
            columns={
                "waktu": "Waktu",
                "aksi": "Keputusan AI",
                "cuaca": "Cuaca",
                "kelembapan_udara": "Kelembapan Udara",
                "suhu_tanah_estimasi": "Estimasi Suhu Tanah"
            }
        )
        st.table(df_log_ai.iloc[::-1].reset_index(drop=True))
    else:
        st.info("Belum ada catatan keputusan AI dalam sesi ini.")

st.markdown("---")

# ============================================================
# 4. KONTROL MANUAL POMPA (Override)
# ============================================================
st.markdown("### 🎮 Remote Control Manual Pompa Air")
st.write("Gunakan tombol berikut untuk mengontrol pompa secara manual (override AI).")

if "log_pompa" not in st.session_state:
    st.session_state.log_pompa = []

col_on, col_off = st.columns(2)

with col_on:
    if st.button("Nyalakan Pompa Air ✔️", use_container_width=True, type="primary"):
        try:
            requests.put(f"{FIREBASE_URL}/kontrol.json", json.dumps({"pompa": 1}), timeout=3)
        except Exception:
            pass
        st.session_state.pompa_status = "MENYALA 🔥"
        st.session_state.log_pompa.append({
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "aksi": "🟢 NYALA",
            "kelembapan": f"{kelembapan_tanah} %",
            "suhu_tanah": f"{temperatur_tanah} °C",
            "suhu_udara": f"{suhu_udara} °C",
            "cuaca": prediksi_cuaca
        })
        st.success("✅ Perintah 'NYALA' dikirim ke alat!")

with col_off:
    if st.button("Matikan Pompa Air ❌", use_container_width=True):
        try:
            requests.put(f"{FIREBASE_URL}/kontrol.json", json.dumps({"pompa": 0}), timeout=3)
        except Exception:
            pass
        st.session_state.pompa_status = "MATI 🛑"
        st.session_state.log_pompa.append({
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "aksi": "🔴 MATI",
            "kelembapan": f"{kelembapan_tanah} %",
            "suhu_tanah": f"{temperatur_tanah} °C",
            "suhu_udara": f"{suhu_udara} °C",
            "cuaca": prediksi_cuaca
        })
        st.error("🛑 Perintah 'MATI' dikirim ke alat!")

st.markdown("---")

# ============================================================
# 5. LOG RIWAYAT KONTROL POMPA
# ============================================================
st.markdown("### 📋 Riwayat Kontrol Pompa")

if st.session_state.log_pompa:
    for log in reversed(st.session_state.log_pompa):
        st.write(
            f"**{log['waktu']}** — {log['aksi']} &nbsp;|&nbsp; "
            f"Kelem. Tanah: {log['kelembapan']} &nbsp;|&nbsp; "
            f"Suhu Tanah: {log['suhu_tanah']} &nbsp;|&nbsp; "
            f"Suhu Udara: {log['suhu_udara']} &nbsp;|&nbsp; "
            f"Cuaca: {log['cuaca']}"
        )
else:
    st.info("Belum ada riwayat kontrol pompa dalam sesi ini.")

st.markdown("---")

# ============================================================
# 6. GRAFIK TREN DATA SENSOR
# ============================================================
st.markdown("### 📈 Grafik Tren Data Sensor (Real-Time)")

# ==========================================
# VISUALISASI GRAFIK TREN (SELALU TAMPIL)
# ==========================================
st.markdown("### 📊 Tren Kelembapan & Suhu Lahan (Real-time)")
col_g1, col_g2 = st.columns(2)

# Konversi data historis menjadi DataFrame untuk Plotly
if not st.session_state.historis:
    import pandas as pd
    from datetime import datetime
    chart_data = pd.DataFrame([{
        "Waktu": datetime.now().strftime("%H:%M:%S"),
        "Kelembapan Tanah (%)": kelembapan_tanah,
        "Suhu Tanah (°C)": temperatur_tanah,
        "Suhu Udara (°C)": suhu_udara
    }])
else:
    import pandas as pd
    chart_data = pd.DataFrame(st.session_state.historis)

# 1. GRAFIK KELEMBAPAN TANAH
with col_g1:
    st.caption("💧 Tren Kelembapan Tanah (%)")
    fig_kelembapan = px.line(chart_data, x="Waktu", y="Kelembapan Tanah (%)", markers=True)
    fig_kelembapan.update_layout(
        yaxis=dict(range=[0, 100], title="Kelembapan (%)"),
        xaxis=dict(title="Waktu"),
        margin=dict(l=24, r=24, t=24, b=24),
        height=260,
        template="plotly_dark"
    )
    st.plotly_chart(fig_kelembapan, use_container_width=True)

# 2. GRAFIK SUHU TANAH & UDARA
with col_g2:
    st.caption("🌡️ Tren Suhu Lahan (°C)")
    fig_suhu = px.line(chart_data, x="Waktu", y=["Suhu Tanah (°C)", "Suhu Udara (°C)"], markers=True)
    fig_suhu.update_layout(
        yaxis=dict(title="Suhu (°C)"),
        xaxis=dict(title="Waktu"),
        margin=dict(l=24, r=24, t=24, b=24),
        height=260,
        template="plotly_dark"
    )
    st.plotly_chart(fig_suhu, use_container_width=True)

st.markdown("---")

# ==========================================
# REKOMENDASI & KEPUTUSAN AI (ALERT INFORMATIF)
# ==========================================
st.subheader("🤖 Rekomendasi & Keputusan AI:")

if kelembapan_tanah > 70 or prediksi_cuaca in ["Gerimis/Hujan Ringan", "Hujan Lebat"]:
    st.info("💡 **KEPUTUSAN AI:** TUTUP SALURAN AIR 🛑 — *Tindakan efisiensi cerdas dilakukan karena lahan sudah cukup basah atau terdeteksi hujan.*")
    status_sekarang = "TUTUP SALURAN AIR 🛑"
else:
    st.success("💡 **KEPUTUSAN AI:** BUKA SALURAN AIR 💧 — *Lahan membutuhkan irigasi optimal.*")
    status_sekarang = "BUKA SALURAN AIR 💧"

# ==========================================
# PEREKAM LOG OTOMATIS AI (POIN 4)
# ==========================================
from datetime import datetime
waktu_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Catat log jika belum ada data atau keputusannya berubah
if "log_ai" in st.session_state:
    if not st.session_state.log_ai or st.session_state.log_ai[-1]["Keputusan"] != status_sekarang:
        st.session_state.log_ai.append({
            "Waktu": waktu_log,
            "Keputusan": status_sekarang,
            "Kelembapan Lahan": f"{kelembapan_tanah}%",
            "Cuaca": prediksi_cuaca
        })

# Tampilkan Expander Tabel Riwayat Log
with st.expander("📜 Riwayat & Log Keputusan Otomatis AI", expanded=False):
    if "log_ai" in st.session_state and st.session_state.log_ai:
        df_log_ai = pd.DataFrame(st.session_state.log_ai)
        st.dataframe(df_log_ai.iloc[::-1], use_container_width=True)
    else:
        st.caption("Belum ada riwayat keputusan otomatis yang tercatat.")