import streamlit as st
from datetime import date, datetime
import time
import os
import pytz
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="TOJI MODE PRO", page_icon="🦾", layout="centered")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .stExpander { border: 1px solid #444; border-radius: 8px; background-color: #161b22; margin-bottom: 10px; }
    div.stButton > button:first-child { 
        background-color: #d32f2f; 
        color: white; 
        border: none; 
        font-weight: bold; 
        width: 100%; 
        height: 3em;
        font-size: 1.2em;
    }
    .stProgress > div > div > div > div { background-color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# --- PERSISTENCIA DE DATOS (RACHA) ---
DB_FILE = "progreso_toji.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"fecha_inicio_racha": str(date.today())}

def guardar_datos(datos):
    with open(DB_FILE, "w") as f:
        json.dump(datos, f, indent=4)

if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = cargar_datos()

# --- TIEMPO Y RACHA (TIJUANA) ---
tz = pytz.timezone('America/Tijuana') 
hoy_tj = datetime.now(tz)
fecha_str = hoy_tj.strftime("%Y-%m-%d")
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", 
           "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
dia_actual = dias_es.get(hoy_tj.strftime("%A"), "Lunes")

fecha_inicio_obj = datetime.strptime(st.session_state.datos_usuario.get("fecha_inicio_racha", str(date.today())), "%Y-%m-%d").date()
racha = (hoy_tj.date() - fecha_inicio_obj).days + 1

# --- HEADER ---
st.title("🔥 TOJI MODE: OVERDRIVE 🦾")
c_r1, c_r2 = st.columns(2)
with c_r1:
    st.metric("RACHA ACTUAL", f"{racha} DÍAS 🔥")
with c_r2:
    st.subheader(f"📍 {dia_actual}")
    st.caption(hoy_tj.strftime('%d/%m/%Y'))

# --- RUTINA ACTUALIZADA ---
rutinas = {
    "Lunes": [
        ("Press de Banca Recto", "4 × 15", 90, "Pecho"),
        ("Press Inclinado (Pies elevados)", "4 × 15", 90, "Pecho Sup."),
        ("Press Declinado", "4 × 15", 90, "Pecho Inf."),
        ("Press Rotacional (Giro muñeca)", "3 × 15", 60, "Pecho Detalle"),
        ("Rompecráneos (Barra Z)", "4 × 15", 60, "Tríceps"),
        ("Copa de Tríceps", "3 × 15", 60, "Tríceps")
    ],
    "Martes": [
        ("Remo Inclinado", "4 × 15", 90, "Espalda"),
        ("Peso Muerto Rumano", "3 × 12", 90, "Isquios/Espalda"),
        ("Bíceps Barra Z (Abierto)", "4 × 12", 60, "Bíceps (Cabeza corta)"),
        ("Bíceps Barra Z (Cerrado)", "4 × 12", 60, "Bíceps (Cabeza larga)"),
        ("Bíceps Martillo (Barra Z)", "3 × 15", 60, "Braquial"),
        ("Elevación de Piernas", "4 × 20", 45, "Abdomen")
    ],
    "Miércoles": [
        ("Elevaciones Laterales", "5 × 20", 45, "Hombro Lateral"),
        ("Press Militar", "4 × 12", 90, "Hombro Frontal"),
        ("Remo al Mentón (Barra Z)", "3 × 15", 60, "Trapecio/Hombro"),
        ("Crunch con Peso", "4 × 20", 60, "Abdomen"),
        ("Vacío Abdominal", "4 × 30 seg", 30, "Core Interno")
    ],
    "Jueves": [
        ("Hex Press", "4 × 15", 60, "Pecho (Apretando)"),
        ("Rompecráneos", "3 × 15", 60, "Tríceps"),
        ("Bíceps Barra Z (Lento)", "3 × 12", 60, "Bíceps Control"),
        ("Fondos en Banco", "3 × fallo", 60, "Tríceps"),
        ("Flexiones Diamante", "3 × fallo", 60, "Pecho/Tríceps")
    ],
    "Viernes": [
        ("Sentadilla tras nuca", "5 × 12-15", 120, "Pierna Global"),
        ("Peso Muerto Convencional", "3 × 8 (125 lb)", 120, "Cadena Post."),
        ("Flexiones Normales", "3 × fallo", 60, "Cierre Pecho")
    ]
}

# --- LÓGICA DE NAVEGACIÓN ---
dias_entreno = list(rutinas.keys())
es_descanso = dia_actual not in dias_entreno

if "overdrive" not in st.session_state: st.session_state.overdrive = False

if es_descanso and not st.session_state.overdrive:
    st.info(f"🛌 Hoy {dia_actual} es descanso. Recupera el cuerpo.")
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
    st.subheader("Entrenamiento del Día")
    
    for nombre, reps, desc, musculo in ejercicios:
        with st.expander(f"🏋️ {nombre} ({reps})"):
            st.write(f"🎯 **Enfoque:** {musculo}")
            st.write(f"⏱️ **Descanso:** {desc} segundos")
            
            # Botón único para terminar serie y descansar
            if st.button(f"✅ FINALIZAR SERIE", key=f"btn_{nombre}"):
                msg = st.empty()
                bar = st.progress(0)
                # Sonido o aviso visual de inicio
                for s in range(desc, -1, -1):
                    msg.subheader(f"⏳ DESCANSO: {s}s")
                    bar.progress((desc - s) / desc)
                    time.sleep(1)
                
                msg.success("💪 ¡DALE A LA SIGUIENTE SERIE!")
                st.balloons()
                time.sleep(2)
                st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Gestión")
    if st.button("🔴 REINICIAR RACHA"):
        st.session_state.datos_usuario["fecha_inicio_racha"] = str(date.today())
        guardar_datos(st.session_state.datos_usuario)
        st.success("Racha reiniciada")
        st.rerun()
    
    st.divider()
    st.caption("TOJI MODE PRO - Sin excusas.")
        st.rerun()
    if st.button("🔄 Borrar Historial"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.rerun()
