import streamlit as st
from datetime import date, datetime
import time
import os
import pytz
import json
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="TOJI MODE PRO", page_icon="🦾", layout="centered")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .stExpander { border: 1px solid #444; border-radius: 8px; background-color: #161b22; margin-bottom: 10px; }
    div.stButton > button:first-child { background-color: #d32f2f; color: white; border: none; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# --- PERSISTENCIA DE DATOS ---
DB_FILE = "progreso_toji.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"historial": [], "fecha_inicio_racha": str(date.today())}

def guardar_datos(datos):
    with open(DB_FILE, "w") as f:
        json.dump(datos, f, indent=4)

datos_usuario = cargar_datos()

# --- TIEMPO Y RACHA (TIJUANA) ---
tz = pytz.timezone('America/Tijuana') 
hoy_tj = datetime.now(tz)
fecha_str = hoy_tj.strftime("%Y-%m-%d")
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", 
           "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
dia_actual = dias_es.get(hoy_tj.strftime("%A"), "Lunes")

fecha_inicio_obj = datetime.strptime(datos_usuario.get("fecha_inicio_racha", str(date.today())), "%Y-%m-%d").date()
racha = (hoy_tj.date() - fecha_inicio_obj).days + 1

# --- HEADER ---
st.title("🔥 TOJI MODE: OVERDRIVE 🦾")
c_r1, c_r2 = st.columns(2)
with c_r1:
    st.metric("RACHA ACTUAL", f"{racha} DÍAS 🔥")
with c_r2:
    st.subheader(f"📍 {dia_actual}")
    st.caption(hoy_tj.strftime('%d/%m/%Y'))

# --- RUTINA ACTUALIZADA (SIN POLEAS) ---
rutinas = {
    "Lunes": [
        ("Press de Banca con Barra", "4 × 10 (Excén. 3s)", 120, "banca.mp4", "Pecho"),
        ("Remo con Barra (Inclinado)", "4 × 10", 90, "remo_barra.mp4", "Espalda"),
        ("Press Militar Mancuerna (Sentado)", "3 × 10", 90, "militar_man.mp4", "Hombros"),
        ("Remo Vertical Barra (Ancho)", "3 × 12", 60, "remo_vertical.mp4", "Trapecio/Hombro"),
        ("Curl de Bíceps con Barra", "3 × 12 (Controlado)", 60, "curl_barra.mp4", "Bíceps"),
        ("Press Francés con Barra", "3 × 12", 60, "frances.mp4", "Tríceps")
    ],
    "Martes": [
        ("Sentadilla con Barra", "4 × 10-12", 120, "sentadilla.mp4", "Cuádriceps"),
        ("Extensión de Pierna (Banco)", "4 × 15 (Pausa 2s)", 90, "extension.mp4", "Cuádriceps"),
        ("Zancadas (Lunges) Manc.", "3 × 12 pasos", 90, "zancadas.mp4", "Pierna Global"),
        ("Peso Muerto Rumano", "3 × 12", 90, "rumano.mp4", "Isquiotibiales"),
        ("Pantorrilla de pie (Escalón)", "4 × 20", 60, "pantorrilla_pie.mp4", "Pantorrillas")
    ],
    "Miércoles": [
        ("Vuelos Posteriores (Pájaros)", "4 × 20", 60, "pajaros.mp4", "Hombro Post."),
        ("Elevaciones Laterales", "4 × 15", 60, "laterales.mp4", "Hombro Lat."),
        ("Pull-over con Mancuerna", "3 × 12", 90, "pullover.mp4", "Dorsal/Pecho"),
        ("Caminata de Granjero", "3 × 1 min", 90, "granjero.mp4", "Core/Agarre"),
        ("Plancha Abdominal", "3 × 1 min", 60, "plancha.mp4", "Abdominales"),
        ("Y-W-T (Isométricos)", "2 rondas 30s c/u", 30, "ywt.mp4", "Postura")
    ],
    "Jueves": [
        ("Remo Mancuerna a una mano", "4 × 10 por lado", 60, "remo_man.mp4", "Espalda"),
        ("Press Inclinado Mancuernas", "3 × 12 (30°)", 90, "inclinado_man.mp4", "Pecho Sup."),
        ("Flexiones (Lagartijas)", "3 × al fallo", 60, "flexiones.mp4", "Pecho/Tríceps"),
        ("Elevaciones Frontales Manc.", "3 × 12", 60, "frontales.mp4", "Hombro Ant."),
        ("Martillos (Mancuerna)", "3 × 12", 60, "martillo.mp4", "Bíceps/Braquial"),
        ("Copa de Tríceps", "3 × 12", 60, "copa.mp4", "Tríceps")
    ],
    "Viernes": [
        ("Hip Thrust con Barra", "4 × 12", 120, "hip_thrust.mp4", "Glúteo"),
        ("Sentadilla Búlgara", "3 × 10 por pierna", 90, "bulgara.mp4", "Glúteo/Pierna"),
        ("Extensión de Pierna (Banco)", "3 × 20 (Bombeo)", 60, "extension_light.mp4", "Cuádriceps"),
        ("Pantorrilla sentado", "4 × 20 (Discos)", 60, "pantorrilla_sentado.mp4", "Pantorrillas")
    ]
}

# --- LÓGICA DE NAVEGACIÓN ---
dias_entreno = list(rutinas.keys())
es_descanso = dia_actual not in dias_entreno

if "overdrive" not in st.session_state: st.session_state.overdrive = False

if es_descanso and not st.session_state.overdrive:
    st.info(f"🛌 Hoy {dia_actual} es descanso. Recupera el tendón.")
    if st.button("🔥 ACTIVAR MODO OVERDRIVE"):
        st.session_state.overdrive = True
        st.rerun()
else:
    if st.session_state.overdrive:
        st.warning("⚡ MODO OVERDRIVE ACTIVADO")
        seleccion = st.selectbox("Elige qué sesión hacer:", dias_entreno)
        ejercicios = rutinas[seleccion]
        if st.button("❌ Salir del Overdrive"):
            st.session_state.overdrive = False
            st.rerun()
    else:
        ejercicios = rutinas.get(dia_actual, [])

    # --- LISTA DE EJERCICIOS ---
    for nombre, reps, desc, video_file, musculo in ejercicios:
        with st.expander(f"🏋️ {nombre} ({reps})"):
            st.info(f"🎯 **Enfoque:** {musculo}")
            
            # Video Check
            if os.path.exists(video_file):
                st.video(video_file)
            else:
                st.caption(f"📹 Sube '{video_file}' a GitHub para ver el video.")
            
            # Registro Peso
            col_u, col_p = st.columns([1, 2])
            with col_u:
                unid = st.radio("Unidad", ["Kg", "Lbs"], key=f"u_{nombre}", horizontal=True)
            with col_p:
                val = st.number_input(f"Peso", min_value=0.0, step=0.5, key=f"p_{nombre}")
            
            if st.button(f"Registrar Serie", key=f"btn_{nombre}"):
                peso_kg = round(val / 2.20462, 2) if unid == "Lbs" else val
                datos_usuario["historial"].append({"fecha": fecha_str, "ejercicio": nombre, "peso": peso_kg})
                guardar_datos(datos_usuario)
                
                # Descanso dinámico
                msg = st.empty()
                bar = st.progress(0)
                for s in range(desc, -1, -1):
                    msg.write(f"⏳ Descanso: {s}s")
                    bar.progress((desc - s) / desc)
                    time.sleep(1)
                st.balloons()
                st.rerun()

# --- GRÁFICA ---
st.divider()
if datos_usuario["historial"]:
    df = pd.DataFrame(datos_usuario["historial"])
    df['fecha'] = pd.to_datetime(df['fecha'])
    st.subheader("📈 Progreso de Fuerza")
    ej_sel = st.selectbox("Analizar:", df['ejercicio'].unique())
    st.line_chart(df[df['ejercicio'] == ej_sel].sort_values('fecha').set_index('fecha')['peso'])

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Gestión")
    if st.button("🔴 REINICIAR RACHA"):
        datos_usuario["fecha_inicio_racha"] = str(date.today())
        guardar_datos(datos_usuario)
        st.rerun()
    if st.button("🔄 Borrar Historial"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.rerun()
