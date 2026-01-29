import streamlit as st
from datetime import date, datetime
import time
import os
import pytz

# --- CONFIGURACIÓN DE PESTAÑA E ICONO ---
st.set_page_config(
    page_title="TOJI MODE", 
    page_icon="🦾", 
    layout="centered"
)

# --- LÓGICA DE TIJUANA (Pacific Time) ---
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
st.title("🔥 TOJI MODE: ON 🦾")
st.metric(label="Racha de Entrenamiento", value=f"{racha_actual} Días")
st.subheader(f"📍 Tijuana: {dia_actual_es} {fecha_hoy.strftime('%d/%m/%Y')}")

if "completados" not in st.session_state:
    st.session_state.completados = []

def descanso(nombre, seg):
    p = st.empty()
    for t in range(seg, -1, -1):
        p.subheader(f"⏳ Descanso: {t}s")
        time.sleep(1)
    p.success(f"¡Dale con todo!")
    st.balloons()
    if nombre not in st.session_state.completados:
        st.session_state.completados.append(nombre)
        st.rerun()

# --- RUTINA COMPLETA ---
rutinas = {
    "Lunes": [
        ("Press banca (3x8-10)", 90, "banca.mp4"), 
        ("Press inclinado (2x10)", 90, "inclinado.mp4"),
        ("Flexiones lentas (2x Fallo)", 60, "flexiones.mp4"),
        ("Press militar (2x8)", 90, "militar.mp4"),
        ("Fondos entre bancas (2x12)", 60, "fondos.mp4")
    ],
    "Martes": [
        ("Remo con barra (3x8-10)", 90, "remo_barra.mp4"), 
        ("Peso muerto rumano (2x6-8)", 120, "rumano.mp4"),
        ("Remo con mancuernas (2x10)", 90, "remo_man.mp4"),
        ("Curl bíceps barra (2x10)", 60, "curl_barra.mp4"),
        ("Curl martillo (2x12)", 60, "martillo.mp4")
    ],
    "Miércoles": [
        ("Sentadilla con barra (3x8)", 120, "sentadilla.mp4"),
        ("Sentadilla búlgara (2x12)", 90, "bulgara.mp4"),
        ("Zancadas (2x10)", 90, "zancadas.mp4"),
        ("Elevación talón (2x15)", 60, "talon.mp4"),
        ("Plancha (2x60s)", 45, "plancha.mp4"),
        ("Elevación piernas (2x12)", 45, "elev_piernas.mp4")
    ],
    "Jueves": [
        ("Elevaciones laterales (3x12)", 45, "laterales.mp4"), 
        ("Pájaros (2x12)", 60, "pajaros.mp4"),
        ("Fondos con banca (2x12)", 60, "fondos_banca.mp4"),
        ("Curl concentrado (1x12)", 60, "concentrado.mp4"),
        ("Plancha lateral (2x30s)", 45, "plancha_lat.mp4"),
        ("Crunch lento (2x15)", 45, "crunch.mp4")
    ],
    "Viernes": [
        ("Remo barra ligero (2x12)", 90, "remo_ligero.mp4"), 
        ("Pullover (2x12)", 90, "pullover.mp4"),
        ("Curl bíceps man. (2x12)", 60, "biceps_man.mp4"),
        ("Hollow hold (2x30s)", 45, "hollow.mp4"),
        ("Crunch lento (2x15)", 45, "crunch.mp4")
    ]
}

if dia_actual_es in rutinas:
    for ej, sec, archivo in rutinas[dia_actual_es]:
        hecho = ej in st.session_state.completados
        with st.expander(f"🏋️ {ej}"):
            if os.path.exists(archivo):
                st.video(archivo)
            else:
                st.error(f"Falta archivo: {archivo}")
            
            if st.checkbox(f"Hecho", key=ej, value=hecho, disabled=hecho):
                if not hecho:
                    descanso(ej, sec)
else:
    st.success("¡Día de descanso! 🛌")

st.divider()
if st.button("🔄 Resetear día"):
    st.session_state.completados = []
    st.rerun()
