import streamlit as st
import googleapiclient.discovery
import pandas as pd

st.title("🔥 BABYMONSTER Live Stats")

# Configuración de YouTube
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
    datos = []
    for item in res['items']:
        v_id = item['id']
        nombre_cancion = next((k for k, v in VIDEOS.items() if v == v_id), "N/A")
        datos.append({
            "Cancion": nombre_cancion,
            "Vistas": int(item['statistics']['viewCount'])
        })
    return pd.DataFrame(datos)

# Botón de ejecución
if st.button('🚀 CARGAR VISTAS REALES'):
    df = get_data()
    
    st.subheader("Gráfico de Popularidad")
    # Usamos nombres fijos para evitar el KeyError
    st.bar_chart(data=df, x="Cancion", y="Vistas")
    
    st.subheader("Tabla de Datos")
    st.write(df)
