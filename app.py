import streamlit as st
import googleapiclient.discovery
import pandas as pd

st.set_page_config(page_title="BABYMONSTER Stats", page_icon="🔥")
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
    data = []
    for item in res['items']:
        # Buscamos cuál de nuestros apodos coincide con el ID de YouTube
        v_id = item['id']
        nombre_corto = next((k for k, v in VIDEOS.items() if v == v_id), "Video")
        
        data.append({
            "Cancion": nombre_corto,
            "Vistas": int(item['statistics']['viewCount'])
        })
    return pd.DataFrame(data)

if st.button('🔄 Actualizar Estadísticas'):
    df = get_data()
    # Usamos 'Cancion' como nombre de columna para que no se pierda
    st.bar_chart(df.set_index('Cancion')['Vistas'])
    st.table(df)
else:
    st.info("Toca el botón para ver el alcance de las chicas.")
        
