import streamlit as st
import googleapiclient.discovery
import pandas as pd

st.title("🔥 BABYMONSTER Live Stats")

# Tu llave
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
        # Buscamos el nombre corto
        nombre = "Video"
        for k, v in VIDEOS.items():
            if v == v_id:
                nombre = k
        
        lista_final.append({
            "Video": nombre,
            "Vistas": int(item['statistics']['viewCount'])
        })
    return pd.DataFrame(lista_final)

if st.button('🔄 Ver Estadísticas Reales'):
    df = get_data()
    # Usamos directamente 'Video' que es lo más sencillo
    st.bar_chart(df.set_index('Video'))
    st.table(df)
    
        
