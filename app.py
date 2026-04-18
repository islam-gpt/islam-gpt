import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="IslamGPT", page_icon="🕌", layout="centered")

# CSS ile arka planı ve yazıları biraz güzelleştirelim
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🕌 IslamGPT: Akıllı Bilgi Asistanı")
st.write("Diyanet kaynaklarını ve notlarınızı tarayan yapay zeka.")

# --- FONKSİYONLAR ---

def internetten_ara(soru):
    """İnternet üzerinde Diyanet odaklı arama yapar."""
    sorgu = f"{soru} nedir diyanet"
    url = f"https://html.duckduckgo.com/html/?q={sorgu}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        ozetler = soup.find_all('a', class_='result__snippet')
        
        bilgi = ""
        for o in ozetler[:3]:
            bilgi += f"🔹 {o.get_text().strip()}\n\n"
        return bilgi
    except:
        return None

# --- ARAYÜZ ---

soru = st.text_input("Merak ettiğiniz konuyu yazın:", placeholder="Örn: Namazın vacipleri nelerdir?")

if st.button("Araştırmayı Başlat"):
    if soru:
        with st.spinner('Bilgi kaynakları taranıyor...'):
            # Şimdilik sadece internet araması aktif (GitHub'da Drive bağlantısı zor olduğu için)
            sonuc_web = internetten_ara(soru)
            
            if sonuc_web and len(sonuc_web) > 10:
                st.success("✅ Bilgi Bulundu!")
                st.markdown("### 📜 Kaynak Özeti")
                st.info(sonuc_web)
                st.caption("Kaynak: DuckDuckGo üzerinden Diyanet ve DİA verileri taranmıştır.")
            else:
                st.error("❌ Üzgünüm, bu konuda net bir özet bilgiye ulaşılamadı.")
    else:
        st.warning("Lütfen bir soru yazın.")

st.markdown("---")
st.markdown("<center>IslamGPT v1.0 | 2026</center>", unsafe_allow_html=True)