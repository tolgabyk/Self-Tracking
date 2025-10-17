import streamlit as st
import pandas as pd
from datetime import datetime
from data_handler import save_activity, load_data
from analysis import analyze_week_gemini, plot_activity_stats

st.set_page_config(page_title="Zaman Çizelgesi Analizörü", page_icon="🧠", layout="wide")

st.title("🧭 Zaman Çizelgesi Analizörü (AI Destekli)")
st.write("Her gün yaptıklarını kaydet, haftalık sürecini analiz et ve Gemini'den kişisel tavsiye al!")


col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Günlük Aktivite Girişi")

    date = st.date_input("Tarih", datetime.today())
    activity = st.text_area("Bugün neler yaptın?", placeholder="Örneğin: Ders çalıştım, yürüyüşe çıktım, film izledim...")

    if st.button("💾 Kaydet"):
        if activity.strip():
            save_activity(date, activity)
            st.success("Aktivite başarıyla kaydedildi ✅")
        else:
            st.warning("Lütfen bir aktivite gir.")

with col2:
    st.subheader("📊 Haftalık Aktivite Verileri")
    df = load_data()

    if not df.empty:
        st.dataframe(df.tail(7), use_container_width=True)
        plot_activity_stats(df)
    else:
        st.info("Henüz veri bulunamadı. Aktivite kaydederek başlayabilirsin.")

# --- Haftalık Analiz ---
st.subheader("🧩 Haftalık AI Analizi (Gemini)")

if st.button("🚀 Haftalık Analizi Başlat"):
    if not df.empty:
        with st.spinner("Gemini haftanı analiz ediyor... ⏳"):
            summary = analyze_week_gemini(df)
        st.markdown(summary)
    else:
        st.warning("Analiz için en az birkaç günlük veri girmelisin.")
