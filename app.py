
import streamlit as st
import requests

# Set judul halaman web
st.set_page_config(page_title="AgriTech Bantul", page_icon="🌱", layout="centered")

st.title("🌱 Sistem Pemantauan Lahan AI")
st.subheader("📍 Pulokadang RT 02, Canden, Jetis, Bantul")

st.markdown("---")

# Koordinat Jetis, Bantul
LATITUDE = "-7.9056"
LONGITUDE = "110.3703"

if st.button("🔄 Cek Kondisi Cuaca & Lahan Terbaru"):
    with st.spinner("Menghubungkan ke satelit..."):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,rain&timezone=Asia%2FBangkok"
        
        try:
            response = requests.get(url).json()
            data_sekarang = response['current']
            suhu_live = data_sekarang['temperature_2m']
            kelembapan_live = data_sekarang['relative_humidity_2m']
            hujan_live = data_sekarang['rain']
            
            # Tampilan Box Informasi (Metrik) di Website
            col1, col2, col3 = st.columns(3)
            col1.metric("🌡️ Suhu", f"{suhu_live}°C")
            col2.metric("💧 Kelembapan", f"{kelembapan_live}%")
            col3.metric("🌧️ Curah Hujan", f"{hujan_live} mm")
            
            st.markdown("---")
            st.subheader("🤖 Rekomendasi AI:")
            
            # Logika keputusan AI
            if suhu_live > 31.0 and hujan_live == 0:
                st.error("🚨 PERINGATAN: Cuaca di Jetis sedang terik dan kering. AI menyarankan cek kelembapan tanah, nyalakan pompa jika tanah mulai mengeras.")
            elif hujan_live > 0:
                st.success("🌧️ INFO: Sedang terdeteksi hujan di wilayah Anda. MATIKAN POMPA AIR, manfaatkan air hujan untuk menghemat listrik.")
            else:
                st.info("✅ INFO: Kondisi cuaca Jetis terpantau normal. Lakukan penyiraman rutin harian secara berkala.")
                
        except Exception as e:
            st.error("❌ Gagal mengambil data satelit. Coba beberapa saat lagi.")
