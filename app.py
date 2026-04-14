import streamlit as st
import googleapiclient.discovery
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BAEMON Live Stats", layout="wide", page_icon="🔥")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuración")
filtro_vistas = st.sidebar.slider("Filtrar por mínimo de vistas (M)", 0, 500, 0)

# --- TÍTULO ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💎 BABYMONSTER Global Analytics</h1>", unsafe_allow_html=True)

# 🔥 DEBUG SECRETS
st.write("DEBUG SECRETS:", st.secrets)

st.markdown("<p style='text-align: center;'>Datos en tiempo real</p>", unsafe_allow_html=True)
st.markdown("---")

# --- CLIENTE YOUTUBE ---
@st.cache_resource
def get_yt_client():
    API_KEY = st.secrets["API_KEY"]
    return googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

yt = get_yt_client()

# --- VIDEOS ---
VIDEOS = {
    "SHEESH": "2wA_b6asW8Y",
    "BATTER UP": "olDWmC0m0u0",
    "FOREVER": "9H77pG8vE6Q",
    "DRIP": "jM9uS6UuXk8"
}

# 🚨 FUNCIÓN SIN TRY/EXCEPT (para ver error real)
@st.cache_data(ttl=300)
def get_data():
    ids = ",".join(VIDEOS.values())
    
    res = yt.videos().list(
        part="statistics,snippet",
        id=ids
    ).execute()

    # 🔥 MOSTRAR RESPUESTA DE LA API
    st.write("RESPUESTA API:", res)

    datos = []
    for item in res['items']:
        v_id = item['id']
        nombre = next((k for k, v in VIDEOS.items() if v == v_id), "N/A")
        vistas = int(item['statistics'].get('viewCount', 0))

        datos.append({
            "Canción": nombre,
            "Vistas": vistas
        })

    return pd.DataFrame(datos)

# --- CARGA ---
df = get_data()

# --- UI ---
if not df.empty:

    limite = filtro_vistas * 1_000_000
    df_filtrado = df[df["Vistas"] >= limite]

    if df_filtrado.empty:
        st.warning(f"No hay videos con más de {filtro_vistas}M de vistas")
        st.stop()

    df_sorted = df_filtrado.sort_values("Vistas", ascending=False)

    total_vistas = df["Vistas"].sum()
    top_song = df.sort_values("Vistas", ascending=False).iloc[0]

    if len(df) > 1:
        top_2 = df.sort_values("Vistas", ascending=False).iloc[1]
        diff = top_song["Vistas"] - top_2["Vistas"]
    else:
        diff = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Vistas Totales", f"{total_vistas:,}".replace(",", "."))
    col2.metric("🏆 #1", top
