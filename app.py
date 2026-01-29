import streamlit as st
from datetime import date, datetime
import time
import os
import pytz

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TOJI MODE", page_icon="🦾", layout="centered")

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

st.title("🔥 TOJI MODE: ON 🦾")
st.metric(label="Racha de Entrenamiento", value=f"{racha_actual} Días")
st.subheader(f"📍 {dia_actual_es} {fecha_hoy.strftime('%d/%m/%Y')}")

if "completados" not in st.session_state:
    st.session_state.completados = []

# --- FUNCIÓN PARA BUSCAR ARCHIVOS REBELDES ---
def buscar_video(nombre_buscado):
    archivos_en_carpeta = os.listdir('.')
    # Intenta encontrar el archivo ignorando mayúsculas/minúsculas
    for f in archivos_en_carpeta:
        if f.lower() == nombre_buscado.lower():
            return f
    return None

def descanso(nombre, seg):
    p = st.empty()
    for t in range(seg, -1, -1):
        p.subheader(f"⏳ Descanso: {t}s")
        time.sleep(1)
    p.success("¡Dale!")
    st.balloons()
    if nombre not in st.session_state.completados:
        st.session_state.completados.append(nombre)
        st.rerun()

# --- RUTINA ---
rutinas = {
    "Lunes": [("Press banca", 90, "banca.mp4"), ("Press militar", 90, "militar.mp4"), ("Flexiones", 60, "flexiones.mp4"), ("Inclinado", 90, "inclinado.mp4"), ("Fondos", 60, "fondos.mp4")],
    "Martes": [("Remo barra", 90, "remo_barra.mp4"), ("Peso muerto", 120, "rumano.mp4"), ("Remo mancuerna", 90, "remo_man.mp4"), ("Curl barra", 60, "curl_barra.mp4"), ("Martillo", 60, "martillo.mp4")],
    "Miércoles": [("Sentadilla", 120, "sentadilla.mp4"), ("Búlgara", 90, "bulgara.mp4"), ("Zancadas", 90, "zancadas.mp4"), ("Talón", 60, "talon.mp4"), ("Plancha", 45, "plancha.mp4"), ("Elev. Piernas", 45, "elev_piernas.mp4")],
    "Jueves": [("Laterales", 45, "laterales.mp4"), ("Pájaros", 60, "pajaros.mp4"), ("Fondos banca", 60, "fondos_banca.mp4"), ("Concentrado", 60, "concentrado.mp4"), ("Plancha lateral", 45, "plancha_lat.mp4"), ("Crunch", 45, "crunch.mp4")],
    "Viernes": [("Remo ligero", 90, "remo_ligero.mp4"), ("Pullover", 90, "pullover.mp4"), ("Bíceps man.", 60, "biceps_man.mp4"), ("Hollow hold", 45, "hollow.mp4"), ("Crunch", 45, "crunch.mp4")]
}

if dia_actual_es in rutinas:
    for ej, sec, archivo_nom in rutinas[dia_actual_es]:
        hecho = ej in st.session_state.completados
        with st.expander(f"🏋️ {ej}"):
            # BUSQUEDA INTELIGENTE
            archivo_real = buscar_video(archivo_nom)
            
            if archivo_real:
                st.video(archivo_real)
            else:
                st.error(f"❌ No se encuentra: {archivo_nom}")
                st.write(f"📂 En tu GitHub solo veo: {[f for f in os.listdir('.') if '.mp4' in f.lower()]}")
            
            if st.checkbox(f"Hecho", key=ej, value=hecho, disabled=hecho):
                if not hecho:
                    descanso(ej, sec)
else:
    st.success("¡Descanso! 🛌")

if st.button("🔄 Reset"):
    st.session_state.completados = []
    st.rerun()
