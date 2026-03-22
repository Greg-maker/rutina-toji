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
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .stExpander { border: 1px solid #444; border-radius: 8px; background-color: #161b22; }
    div.stButton > button:first-child { background-color: #d32f2f; color: white; border-radius: 5px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS LOCAL (JSON) ---
DB_FILE = "progreso_toji.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {"historial": []}
    return {"historial": []}

def guardar_datos(datos):
    with open(DB_FILE, "w") as f:
        json.dump(datos, f, indent=4)

datos_usuario = cargar_datos()

# --- LÓGICA DE TIEMPO (TIJUANA) ---
tz = pytz.timezone('America/Tijuana') 
hoy_tj = datetime.now(tz)
fecha_str = hoy_tj.strftime("%Y-%m-%d")
dia_semana = hoy_tj.strftime("%A")

dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", 
           "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
dia_actual = dias_es.get(dia_semana, "Lunes")

# --- RUTINAS ---
rutinas = {
    "Lunes": [
        ("Press de Banca", "4 × 8–10", 120, "Pecho/Tríceps"),
        ("Remo con Barra", "4 × 10", 90, "Espalda"),
        ("Press Militar", "3 × 10", 90, "Hombros"),
        ("Curl de Bíceps", "3 × 12", 60, "Bíceps"),
        ("Press Francés", "3 × 12", 60, "Tríceps")
    ],
    "Martes": [
        ("Sentadilla Barra", "4 × 10", 120, "Piernas"),
        ("Peso Muerto Rumano", "4 × 12", 90, "Isquios"),
        ("Zancadas", "3 × 10", 90, "Glúteo/Pierna"),
        ("Elevación Talones", "4 × 15", 60, "Pantorrillas")
    ],
    "Jueves": [
        ("Press Inclinado", "4 × 12", 90, "Pecho Superior"),
        ("Remo a una mano", "4 × 12", 60, "Espalda"),
        ("Vuelos Laterales", "3 × 15", 60, "Hombro Lateral"),
        ("Martillo Manc.", "3 × 12", 60, "Braquial"),
        ("Fondos", "3 × fallo", 60, "Tríceps")
    ],
    "Viernes": [
        ("Sentadilla Búlgara", "3 × 10", 90, "Cuádriceps"),
        ("Step-ups", "3 × 12", 60, "Piernas"),
        ("Banca Cerrado", "3 × 12", 90, "Tríceps"),
        ("Remo Vertical", "3 × 12", 60, "Trapecios")
    ]
}

# --- HEADER ---
st.title("🔥 TOJI MODE: OVERDRIVE 🦾")
fecha_inicio = date(2026, 1, 28)
racha = (hoy_tj.date() - fecha_inicio).days + 1

col_a, col_b = st.columns(2)
with col_a:
    st.metric("RACHA", f"{racha} DÍAS")
with col_b:
    st.subheader(f"📍 {dia_actual}")
    st.caption(hoy_tj.strftime('%d/%m/%Y'))

# --- LÓGICA DE DÍAS Y OVERDRIVE ---
dias_entreno = ["Lunes", "Martes", "Jueves", "Viernes"]
es_descanso = dia_actual not in dias_entreno

if "overdrive" not in st.session_state:
    st.session_state.overdrive = False

# --- SELECCIÓN DE RUTINA ---
ejercicios_hoy = []
titulo_entreno = ""

if es_descanso and not st.session_state.overdrive:
    st.info("🛌 Hoy es descanso programado. El cuerpo de un Zenin necesita recuperarse.")
    if st.button("🔥 ACTIVAR MODO OVERDRIVE"):
        st.session_state.overdrive = True
        st.rerun()
else:
    if st.session_state.overdrive:
        st.warning("⚡ MODO OVERDRIVE ACTIVADO")
        seleccion = st.selectbox("Elige rutina:", dias_entreno)
        ejercicios_hoy = rutinas[seleccion]
        titulo_entreno = f"Overdrive: {seleccion}"
        if st.button("❌ Desactivar Overdrive"):
            st.session_state.overdrive = False
            st.rerun()
    else:
        ejercicios_hoy = rutinas.get(dia_actual, [])
        titulo_entreno = f"Rutina de {dia_actual}"

# --- LISTA DE EJERCICIOS ---
if ejercicios_hoy:
    st.divider()
    # Para ver los músculos a trabajar hoy
    st.write(f"### {titulo_entreno}")
    
    for nombre, reps, desc, musculo in ejercicios_hoy:
        with st.expander(f"🏋️ {nombre} ({reps})"):
            st.write(f"🎯 **Objetivo:** {musculo}")
            
            c1, c2 = st.columns(2)
            with c1:
                peso = st.number_input(f"Peso (kg)", min_value=0.0, step=0.5, key=f"p_{nombre}")
            with c2:
                if st.button(f"Registrar Serie", key=f"btn_{nombre}"):
                    nuevo = {"fecha": fecha_str, "ejercicio": nombre, "peso": peso}
                    datos_usuario["historial"].append(nuevo)
                    guardar_datos(datos_usuario)
                    
                    msg = st.empty()
                    prog = st.progress(0)
                    for s in range(desc, -1, -1):
                        msg.write(f"⏳ Descanso: {s}s")
                        prog.progress((desc - s) / desc)
                        time.sleep(1)
                    msg.success("¡DALE! 🔥")
                    st.balloons()

# --- ANÁLISIS DE PROGRESO ---
st.divider()
st.subheader("📈 Evolución de Fuerza")
if datos_usuario["historial"]:
    df = pd.DataFrame(datos_usuario["historial"])
    df['fecha'] = pd.to_datetime(df['fecha'])
    lista_ejercicios = df['ejercicio'].unique()
    sel_ej = st.selectbox("Ver evolución de:", lista_ejercicios)
    df_plot = df[df['ejercicio'] == sel_ej].sort_values('fecha')
    st.line_chart(df_plot.set_index('fecha')['peso'])
else:
    st.caption("Aún no hay datos. Registra tu primera serie para ver la gráfica.")

with st.sidebar:
    if st.button("🔄 Borrar Historial"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
