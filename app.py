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
            pass
    return {"historial": [], "fecha_inicio_racha": str(date.today())}

def guardar_datos(datos):
    with open(DB_FILE, "w") as f:
        json.dump(datos, f, indent=4)

datos_usuario = cargar_datos()

# --- LÓGICA DE TIEMPO ---
tz = pytz.timezone('America/Tijuana') 
hoy_tj = datetime.now(tz)
fecha_str = hoy_tj.strftime("%Y-%m-%d")
dia_actual = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", 
              "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}.get(hoy_tj.strftime("%A"), "Lunes")

# --- RUTINAS (Simplificadas para el código) ---
rutinas = {
    "Lunes": [("Press de Banca", "4×8", 120, "Pecho"), ("Remo con Barra", "4×10", 90, "Espalda"), ("Press Militar", "3×10", 90, "Hombros")],
    "Martes": [("Sentadilla Barra", "4×10", 120, "Piernas"), ("Peso Muerto Rumano", "4×12", 90, "Isquios"), ("Zancadas", "3×10", 90, "Pierna")],
    "Jueves": [("Press Inclinado", "4×12", 90, "Pecho Sup"), ("Remo a una mano", "4×12", 60, "Espalda"), ("Vuelos Laterales", "3×15", 60, "Hombro")],
    "Viernes": [("Sentadilla Búlgara", "3×10", 90, "Piernas"), ("Step-ups", "3×12", 60, "Piernas"), ("Banca Cerrado", "3×12", 90, "Tríceps")]
}

# --- HEADER Y RACHA ---
st.title("🔥 TOJI MODE: OVERDRIVE 🦾")
fecha_inicio_obj = datetime.strptime(datos_usuario.get("fecha_inicio_racha", str(date.today())), "%Y-%m-%d").date()
racha = (hoy_tj.date() - fecha_inicio_obj).days + 1

col_a, col_b = st.columns(2)
with col_a:
    st.metric("RACHA ACTUAL", f"{racha} DÍAS 🔥")
with col_b:
    st.subheader(f"📍 {dia_actual}")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ajustes")
    if st.button("🔴 REINICIAR RACHA"):
        datos_usuario["fecha_inicio_racha"] = str(date.today())
        guardar_datos(datos_usuario)
        st.rerun()

# --- LÓGICA OVERDRIVE ---
dias_entreno = list(rutinas.keys())
es_descanso = dia_actual not in dias_entreno

if "overdrive" not in st.session_state: st.session_state.overdrive = False

if es_descanso and not st.session_state.overdrive:
    st.info("🛌 Día de descanso.")
    if st.button("🔥 ACTIVAR MODO OVERDRIVE"):
        st.session_state.overdrive = True
        st.rerun()
else:
    seleccion = st.selectbox("Rutina:", dias_entreno) if st.session_state.overdrive else dia_actual
    ejercicios_hoy = rutinas.get(seleccion, [])

    # --- ENTRENAMIENTO ---
    for nombre, reps, desc, musculo in ejercicios_hoy:
        with st.expander(f"🏋️ {nombre} ({reps})"):
            u1, u2 = st.columns([2, 1])
            with u2:
                unidad = st.radio("Unidad", ["Kg", "Lbs"], key=f"u_{nombre}", horizontal=True)
            with u1:
                valor_input = st.number_input(f"Peso en {unidad}", min_value=0.0, step=0.5, key=f"p_{nombre}")
            
            if st.button(f"Registrar Serie", key=f"btn_{nombre}"):
                # Convertir a KG para la base de datos si es Lbs
                peso_kg = round(valor_input / 2.20462, 2) if unidad == "Lbs" else valor_input
                
                nuevo = {"fecha": fecha_str, "ejercicio": nombre, "peso": peso_kg, "unidad_orig": unidad, "valor_orig": valor_input}
                datos_usuario["historial"].append(nuevo)
                guardar_datos(datos_usuario)
                
                # Timer
                msg = st.empty()
                prog = st.progress(0)
                for s in range(desc, -1, -1):
                    msg.write(f"⏳ Descanso: {s}s")
                    prog.progress((desc - s) / desc)
                    time.sleep(1)
                st.balloons()
                st.rerun()

# --- PROGRESO ---
st.divider()
st.subheader("📈 Evolución de Fuerza (Kg)")
if datos_usuario["historial"]:
    df = pd.DataFrame(datos_usuario["historial"])
    df['fecha'] = pd.to_datetime(df['fecha'])
    sel_ej = st.selectbox("Gráfica de:", df['ejercicio'].unique())
    df_plot = df[df['ejercicio'] == sel_ej].sort_values('fecha')
    st.line_chart(df_plot.set_index('fecha')['peso'])
