import streamlit as st
from datetime import date, datetime
import time
import os
import pytz
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TOJI MODE", page_icon="🦾", layout="centered")

# --- FRASES MOTIVACIONALES ---
frases = [
    "No te detengas cuando canses, detente cuando hayas terminado. 🦾",
    "El dolor es temporal, el orgullo es para siempre. 🔥",
    "¿Eres el más fuerte porque entrenas, o entrenas porque eres el más fuerte? 💀",
    "Un paso más cerca de la perfección física. 🦍",
    "Tu cuerpo es tu templo, y hoy lo has honrado. 🏛️"
]

# --- LÓGICA TIJUANA ---
tz = pytz.timezone('America/Tijuana') 
hoy_tijuana = datetime.now(tz)
fecha_hoy = hoy_tijuana.date()
fecha_inicio = date(2026, 1, 28) 
racha_actual = (fecha_hoy - fecha_inicio).days + 1

dias_espanol = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}
dia_actual_es = dias_espanol.get(hoy_tijuana.strftime("%A"), "Lunes")

# --- ESTADO DE SESIÓN ---
if "series_completadas" not in st.session_state:
    st.session_state.series_completadas = {}

st.title("🔥 TOJI MODE: ON 🦾")
st.metric(label="Racha de Entrenamiento", value=f"{racha_actual} Días")
st.subheader(f"📍 {dia_actual_es} {fecha_hoy.strftime('%d/%m/%Y')}")

def buscar_video(nombre_buscado):
    archivos_en_carpeta = os.listdir('.')
    for f in archivos_en_carpeta:
        if f.lower() == nombre_buscado.lower():
            return f
    return None

def iniciar_descanso(seg):
    p = st.empty()
    for t in range(seg, -1, -1):
        p.subheader(f"⏳ Descanso: {t}s")
        time.sleep(1)
    p.
