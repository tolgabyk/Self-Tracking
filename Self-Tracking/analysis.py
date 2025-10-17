import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# --- Gemini API Key yükle ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_week_gemini(df):
    df = df.tail(7)
    week_text = "\n".join(df["Aktivite"].tolist())

    prompt = f"""
    Aşağıda bir kullanıcının son 7 gündeki aktiviteleri yer alıyor:

    {week_text}

    Bu aktiviteleri analiz et:
    1. Kullanıcının genel üretkenlik seviyesi nasıl?
    2. Duygu durumu veya ruh hali hakkında ne söylenebilir?
    3. Hangi aktiviteleri artırmalı, hangilerini azaltmalı?
    4. Önümüzdeki hafta için kişisel bir tavsiye ver (maksimum 5 cümle).

    Yanıtını Türkçe, sade ve anlaşılır biçimde yaz.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return f"### 🧠 Gemini Analizi\n\n{response.text}"

import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.patheffects as path_effects

def plot_activity_stats(df):
    df = df.tail(7)
    all_text = " ".join(df["Aktivite"].tolist()).lower()
    words = [w for w in all_text.split() if len(w) > 3]

    word_counts = Counter(words)
    common_words = dict(word_counts.most_common(7))

    if not common_words:
        st.info("Bu hafta analiz edilecek yeterli veri bulunamadı.")
        return

    # --- Grafik verileri ---
    words = list(common_words.keys())
    counts = list(common_words.values())

    # --- Renk paleti (gradient efekti) ---
    cmap = plt.get_cmap("viridis")
    colors = [cmap(i / len(words)) for i in range(len(words))]

    # --- Şekil ve tasarım ---
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(words, counts, color=colors, edgecolor="none", height=0.6)

    # --- Estetik ayarlar ---
    ax.set_title("✨ Bu Haftanın En Çok Tekrarlanan Aktiviteleri", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Tekrar Sayısı", fontsize=11)
    ax.set_ylabel("")
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_facecolor("#f9f9f9")
    fig.patch.set_facecolor("#f9f9f9")

    # --- Bar üzerine sayı yazıları ---
    for bar, count in zip(bars, counts):
        text = ax.text(count + 0.1, bar.get_y() + bar.get_height()/2,
                       f"{count}", va='center', fontsize=10, color="#333", fontweight="bold")
        text.set_path_effects([path_effects.withStroke(linewidth=2, foreground='white')])

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)



    
