import streamlit as st
import googleapiclient.discovery
import pandas as pd

st.title("🔥 BABYMONSTER Live Stats")

API_KEY = "AIzaSyDxzjnwjNf8dRo90y4Yopwr909q_l7qalc"
VIDEOS = {
    "SHEESH": "2wA_b6asW8Y",
    "BATTER UP": "olDWmC0m0u0",
    "FOREVER": "9H77pG8vE6Q",
    "DRIP": "jM9uS6UuXk8"
}

yt = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_data():
    ids = ",".join(VIDEOS.values())
    res = yt.videos().list(part="statistics,snippet", id=ids).execute()
    lista_final = []
    for item in res['items']:
        v_id = item['id']
        nombre = next((k for k, v in VIDEOS.items() if v == v_id), "N/A")
        lista_final.append({
            "Single": nombre,
            "Views": int(item['statistics']['viewCount'])
        })
    return pd.DataFrame(lista_final)

if st.button('🚀 CARGAR VISTAS REALES'):
    df = get_data()
    # Aquí está el truco: usamos 'Single' que es nombre nuevo
    st.bar_chart(df.set_index('Single'))
    st.table(df)
