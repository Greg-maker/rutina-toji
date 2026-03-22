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
    div.stButton > button:first-child { background-color: #d32f2f; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- PERSISTENCIA ---
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

# --- TIEMPO Y RACHA ---
tz = pytz.timezone('America/Tijuana') 
hoy_tj = datetime.now(tz)
fecha_str = hoy_tj.strftime("%Y-%m-%d")
dia_actual = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", 
              "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}.get(hoy_tj.strftime("%A"), "Lunes")

fecha_inicio_obj = datetime.strptime(datos_usuario.get("fecha_inicio_racha", str(date.today())), "%Y-%m-%d").date()
racha = (hoy_tj.date() - fecha_inicio_obj).days + 1

# --- HEADER ---
st.title("🔥 TOJI MODE: OVERDRIVE 🦾")
c_r1, c_r2 = st.columns(2)
with c_r1:
    st.metric("RACHA ACTUAL", f"{racha} DÍAS 🔥")
with c_r2:
    st.subheader(f"📍 {dia_actual}")

# --- RUTINA COMPLETA ---
# Formato: (Nombre, Reps, Descanso, Archivo, Músculo)
rutinas = {
    "Lunes": [
        ("Press de Banca (Barra)", "4 × 8–10", 120, "banca.mp4", "Pecho y Tríceps"),
        ("Remo con Barra (Inclinado)", "4 × 10", 90, "remo_barra.mp4", "Espalda"),
        ("Press Militar", "3 × 8–10", 90, "militar.mp4", "Hombros"),
        ("Curl de Bíceps (Barra)", "3 × 12", 60, "curl_barra.mp4", "Bíceps"),
        ("Press Francés", "3 × 12", 60, "frances.mp4", "Tríceps")
    ],
    "Martes": [
        ("Sentadilla con Barra", "4 × 10–12", 120, "sentadilla.mp4", "Cuádriceps y Glúteo"),
        ("Peso Muerto Rumano", "4 × 12", 90, "rumano.mp4", "Isquiotibiales"),
        ("Zancadas (Lunges)", "3 × 10 por pierna", 90, "zancadas.mp4", "Piernas completas"),
        ("Elevación de Talones", "4 × 15–20", 60, "talon.mp4", "Pantorrillas")
    ],
    "Jueves": [
        ("Press Inclinado (Mancuernas)", "4 × 12", 90, "inclinado.mp4", "Pecho Superior"),
        ("Remo a una mano", "4 × 12 por lado", 60, "remo_man.mp4", "Espalda"),
        ("Vuelos Laterales", "3 × 15", 60, "laterales.mp4", "Hombro Lateral"),
        ("Martillo (Mancuernas)", "3 × 12", 60, "martillo.mp4", "Bíceps/Braquial"),
        ("Fondos en Banco", "3 × al fallo", 60, "fondos_banca.mp4", "Tríceps")
    ],
    "Viernes": [
        ("Sentadilla Búlgara", "3 × 10 por pierna", 90, "bulgara.mp4", "Cuádriceps/Glúteo"),
        ("Step-ups (Subida al banco)", "3 × 12 por pierna", 60, "step_up.mp4", "Piernas"),
        ("Press Banca Cerrado", "3 × 12", 90, "banca_cerrado.mp4", "Tríceps y Pecho"),
        ("Remo Vertical (Barra)", "3 × 12", 60, "remo_vertical.mp4", "Trapecios y Hombros")
    ]
}

# --- LÓGICA DE DÍAS ---
if "overdrive" not in st.session_state: st.session_state.overdrive = False
dias_validos = list(rutinas.keys())
es_descanso = dia_actual not in dias_validos

if es_descanso and not st.session_state.overdrive:
    st.info("🛌 Hoy toca descanso. Recupera tu energía.")
    if st.button("🔥 ACTIVAR MODO OVERDRIVE"):
        st.session_state.overdrive = True
        st.rerun()
else:
    if st.session_state.overdrive:
        st.warning("⚡ MODO OVERDRIVE")
        seleccion = st.selectbox("Elige rutina:", dias_validos)
        ejercicios = rutinas[seleccion]
        if st.button("❌ Salir"):
            st.session_state.overdrive = False
            st.rerun()
    else:
        ejercicios = rutinas.get(dia_actual, [])

    # --- RENDERIZADO ---
    for nombre, reps, desc, video_file, musculo in ejercicios:
        with st.expander(f"🏋️ {nombre} ({reps})"):
            st.write(f"🎯 **Músculo:** {musculo}")
            
            # Función de Video
            if os.path.exists(video_file):
                st.video(video_file)
            else:
                st.caption(f"📹 Video '{video_file}' no encontrado.")
            
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
                
                msg = st.empty()
                bar = st.progress(0)
                for s in range(desc, -1, -1):
                    msg.write(f"⏳ Descanso: {s}s")
                    bar.progress((desc - s) / desc)
                    time.sleep(1)
                st.balloons()
                st.rerun()

# --- PROGRESO ---
st.divider()
if datos_usuario["historial"]:
    df = pd.DataFrame(datos_usuario["historial"])
    df['fecha'] = pd.to_datetime(df['fecha'])
    st.subheader("📈 Progreso de Fuerza (Kg)")
    ej_sel = st.selectbox("Ejercicio:", df['ejercicio'].unique())
    st.line_chart(df[df['ejercicio'] == ej_sel].sort_values('fecha').set_index('fecha')['peso'])

# --- SIDEBAR ---
with st.sidebar:
    if st.button("🔴 REINICIAR RACHA"):
        datos_usuario["fecha_inicio_racha"] = str(date.today())
        guardar_datos(datos_usuario)
        st.rerun()
    if st.button("🔄 Borrar Historial"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.rerun()
