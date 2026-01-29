import streamlit as st
from datetime import date, datetime
import time
import os
import pytz

# Configuración de la página
st.set_page_config(page_title="Toji Mode", page_icon="💪", layout="centered")

# --- LÓGICA DE TIJUANA (Pacific Time) ---
# Forzamos la zona horaria de Tijuana para que no se adelante el día
tz = pytz.timezone('America/Tijuana') 
hoy_tijuana = datetime.now(tz)
fecha_hoy = hoy_tijuana.date()

# Fecha de inicio: 28 de enero de 2026
fecha_inicio = date(2026, 1, 28) 

# Cálculo de racha
racha_actual = (fecha_hoy - fecha_inicio).days + 1

# Traductor de días
dias_espanol = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
dia_semana_ing = hoy_tijuana.strftime("%A")
dia_actual_es = dias_espanol.get(dia_semana_ing, "Lunes")

# --- INTERFAZ ---
st.title("🔥 Toji Mode: On")
st.metric(label="Racha de Entrenamiento", value=f"{racha_actual} Días")
st.subheader(f"📍 Tijuana: {dia_actual_es} {fecha_hoy.strftime('%d/%m/%Y')}")

if "completados" not in st.session_state:
    st.session_state.completados = []

def descanso(nombre, seg):
    p = st.empty()
    for t in range(seg, -1, -1):
        p.subheader(f"⏳ Descanso: {t}s")
        time.sleep(1)
    p.success(f"¡Dale!")
    st.balloons()
    if nombre not in st.session_state.completados:
        st.session_state.completados.append(nombre)
        st.rerun()

# --- RUTINA ---
rutinas = {
    "Lunes": [("Press banca (3x8-10)", 90, "banca.mp4"), ("Press militar (2x8)", 90, "militar.mp4")],
    "Martes": [("Remo con barra (3x8-10)", 90, "remo_barra.mp4"), ("Peso muerto rumano (2x6-8)", 120, "rumano.mp4")],
    "Miércoles": [
        ("Sentadilla con barra (3x8)", 120, "sentadilla.mp4"),
        ("Sentadilla búlgara (2x12)", 90, "bulgara.mp4"),
        ("Zancadas (2x10)", 90, "zancadas.mp4"),
        ("Elevación talón (2x15)", 60, "talon.mp4"),
        ("Plancha (2x60s)", 45, "plancha.mp4"),
        ("Elevación piernas (2x12)", 45, "elev_piernas.mp4")
    ],
    "Jueves": [("Elevaciones laterales (3x12)", 45, "laterales.mp4"), ("Crunch lento (2x15)", 45, "crunch.mp4")],
    "Viernes": [("Remo barra ligero (2x12)", 90, "remo_ligero.mp4"), ("Pullover (2x12)", 90, "pullover.mp4")]
}

if dia_actual_es in rutinas:
    for ej, sec, archivo in rutinas[dia_actual_es]:
        hecho = ej in st.session_state.completados
        with st.expander(f"🏋️ {ej}"):
            if os.path.exists(archivo):
                st.video(archivo)
            else:
                st.error(f"Falta: {archivo}")
            
            if st.checkbox(f"Hecho", key=ej, value=hecho, disabled=hecho):
                if not hecho:
                    descanso(ej, sec)
else:
    st.success("¡Descanso en Tijuana! 🛌")

if st.button("🔄 Reset"):
    st.session_state.completados = []
    st.rerun()
