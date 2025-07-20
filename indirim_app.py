import streamlit as st
from datetime import datetime

st.title("💰 İndirim Hesaplama Programı")

isim = st.text_input("İsim ve Soyisim")
fiyat = st.number_input("Fiyat (TL)", min_value=0.0, step=0.01)
oran = st.number_input("İndirim Oranı (%)", min_value=0.0, step=0.1)

if st.button("Hesapla"):
    try:
        indirim = fiyat * (oran / 100)
        yeni_fiyat = fiyat - indirim
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

        st.success(f"""
        **{isim}**
        \nİndirimli Fiyat: **{yeni_fiyat:.2f} TL**
        \nTarih: {tarih}
        """)
    except Exception:
        st.error("Lütfen geçerli değerler girin!")
