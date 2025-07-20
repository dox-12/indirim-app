import streamlit as st
from datetime import datetime, date

# Uygulama Ayarları
st.set_page_config(page_title="İndirim Hesaplama", page_icon="💰", layout="centered")

# Tema Seçimi
tema = st.radio("Tema Seç:", ["🌞 Light", "🌙 Dark"])
if tema == "🌙 Dark":
    st.markdown(
        """
        <style>
        body { background-color: #222; color: white; }
        </style>
        """, unsafe_allow_html=True
    )

# Logo ve Başlık
st.image("https://cdn-icons-png.flaticon.com/512/1997/1997928.png", width=80)
st.title("💰 İndirim Hesaplama Programı")

# Girdi Alanları
isim = st.text_input("İsim ve Soyisim")
fiyat = st.number_input("Fiyat (TL)", min_value=0.0, step=0.01)
oran = st.number_input("İndirim Oranı (%)", min_value=0.0, step=0.1)

# Hesaplama Geçmişi İçin Session State
if "gecmis" not in st.session_state:
    st.session_state.gecmis = []  # (isim, yeni_fiyat, tarih)

# Hesaplama Butonu
if st.button("Hesapla"):
    try:
        indirim = fiyat * (oran / 100)
        yeni_fiyat = fiyat - indirim
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

        sonuc = (isim, yeni_fiyat, tarih)
        st.success(f"{isim} | İndirimli: {yeni_fiyat:.2f} TL | Tarih: {tarih}")

        # Geçmişe Ekle
        st.session_state.gecmis.append(sonuc)
    except Exception:
        st.error("Lütfen geçerli değerler girin!")

# --- Tarih Filtreleme ---
if st.session_state.gecmis:
    st.subheader("📝 Hesaplama Geçmişi")

    # Tarih filtre seçimi
    baslangic = st.date_input("Başlangıç Tarihi", value=date.today())
    bitis = st.date_input("Bitiş Tarihi", value=date.today())

    # Filtreleme ve gösterme
    for (ad, fiyat, tarih) in st.session_state.gecmis[::-1]:
        tarih_obj = datetime.strptime(tarih, "%d.%m.%Y %H:%M").date()
        if baslangic <= tarih_obj <= bitis:
            st.write(f"- **{ad}** | {fiyat:.2f} TL | {tarih}")
