import streamlit as st
import googleapiclient.discovery
import pandas as pd

st.title("🔥 BABYMONSTER Live Stats")

# 1. Configuración
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
        # Buscamos el nombre de la canción
        nombre_cancion = next((k for k, v in VIDEOS.items() if v == v_id), "N/A")
        # GUARDAMOS CON ESTOS NOMBRES EXACTOS
        datos.append({
            "Cancion": nombre_cancion,
            "Vistas": int(item['statistics']['viewCount'])
        })
    return pd.DataFrame(datos)

# 2. El Botón Mágico
if st.button('🚀 CARGAR VISTAS REALES'):
    df = get_data()
    st.subheader("Gráfico de Vistas")
    # USAMOS LOS MISMOS NOMBRES DE ARRIBA
    st.bar_chart(data=df, x="Cancion", y="Vistas")
    st.subheader("Tabla Detallada")
    st.write(df)
