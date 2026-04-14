import streamlit as st
import googleapiclient.discovery
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BAEMON Live Stats", layout="wide", page_icon="🔥")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuración")
filtro_vistas = st.sidebar.slider("Filtrar por mínimo de vistas (M)", 0, 500, 0)
auto_refresh = st.sidebar.toggle("Auto-refresh cada 5 min")

# --- FORMATO LATAM ---
def format_num(n):
    return f"{n:,}".replace(",", ".")

# --- CLIENTE YOUTUBE OPTIMIZADO ---
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
    "DRIP": "jM9uS6UuXk8",
    "CLIK CLAK": "pS_pYf8-k80"
}

# --- OBTENER DATOS ---
@st.cache_data(ttl=300)
def get_data():
    try:
        ids = ",".join(VIDEOS.values())
        res = yt.videos().list(part="statistics,snippet", id=ids).execute()
        datos = []
        for item in res['items']:
            v_id = item['id']
            nombre = next((k for k, v in VIDEOS.items() if v == v_id), "N/A")
            vistas = int(item['statistics'].get('viewCount', 0))
            datos.append({"Canción": nombre, "Vistas": vistas})
        return pd.DataFrame(datos)
    except Exception as e:
        st.error(f"Error al conectar con YouTube: {e}")
        return pd.DataFrame()

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💎 BABYMONSTER Global Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Datos en tiempo real</p>", unsafe_allow_html=True)
st.markdown("---")

# --- LOADING ---
with st.spinner("Cargando analíticas en tiempo real..."):
    df = get_data()

if not df.empty:

    # --- FILTRO ---
    limite = filtro_vistas * 1_000_000
    df_filtrado = df[df["Vistas"] >= limite]

    if df_filtrado.empty:
        st.warning(f"No hay videos con más de {filtro_vistas}M de vistas")
        st.stop()

    df_sorted = df_filtrado.sort_values("Vistas", ascending=False)

    st.caption(f"Mostrando {len(df_filtrado)} de {len(df)} videos")

    # --- RANKING SEGURO ---
    df_rank = df.sort_values("Vistas", ascending=False)
    top_song = df_rank.iloc[0]

    if len(df_rank) > 1:
        top_2 = df_rank.iloc[1]
        diff = top_song["Vistas"] - top_2["Vistas"]
    else:
        diff = 0

    total_vistas = df["Vistas"].sum()

    # --- MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("📈 Vistas Totales", format_num(total_vistas))
    m2.metric("🏆 #1", top_song["Canción"])
    m3.metric("🔥 Ventaja", format_num(diff))

    # --- DESTACADO ---
    st.markdown(
        f"## 🥇 {top_song['Canción']} — {format_num(top_song['Vistas'])} vistas"
    )

    # --- PROGRESS ---
    max_views = df["Vistas"].max()
    if max_views > 0:
        st.progress(top_song["Vistas"] / max_views)

    st.markdown("---")

    # --- GRÁFICO ---
    st.subheader("📊 Ranking de Popularidad")
    st.bar_chart(df_sorted.set_index("Canción"))

    # --- GOD MODE: VIEWS POR SEGUNDO ---
    if "prev_df" not in st.session_state:
        st.session_state.prev_df = df

    prev_df = st.session_state.prev_df

    try:
        df_merge = df.merge(prev_df, on="Canción", suffixes=("", "_prev"))
        df_merge["Views/s"] = (df_merge["Vistas"] - df_merge["Vistas_prev"]) / 300

        st.subheader("⚡ Crecimiento (Views por segundo)")
        st.dataframe(
            df_merge[["Canción", "Views/s"]].style.format({"Views/s": "{:.2f}"}),
            use_container_width=True,
            hide_index=True
        )
    except:
        pass

    st.session_state.prev_df = df

    # --- TABLA ---
    st.subheader("📝 Datos completos")
    st.dataframe(df_sorted, use_container_width=True, hide_index=True)

    # --- REFRESH ---
    if st.sidebar.button("🔄 Actualizar ahora"):
        st.cache_data.clear()
        st.rerun()

    # --- AUTO REFRESH ---
    if auto_refresh:
        st.cache_data.clear()
        st.rerun()

else:
    st.error("No se pudieron cargar los datos")

st.markdown("---")
st.caption("Dashboard Pro creado por Luis Sequeira 🚀")
