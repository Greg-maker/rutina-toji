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

def buscar_video(nombre_buscado):
    archivos_en_carpeta = os.listdir('.')
    for f in archivos_en_carpeta:
        if f.lower() == nombre_buscado.lower():
            return f
    return None

def descanso(nombre, seg):
    p = st.empty()
    for t in range(seg, -1, -1):
        p.subheader(f"⏳ Descanso: {t}s")
        time.sleep(1)
    p.success("¡Siguiente serie!")
    st.balloons()
    if nombre not in st.session_state.completados:
        st.session_state.completados.append(nombre)
        st.rerun()

# --- RUTINA DETALLADA (Músculos añadidos) ---
# Formato: (Nombre, Reps, Descanso, Archivo, Músculo principal)
rutinas = {
    "Lunes": [
        ("Press banca", "3 × 8–10", 90, "banca.mp4", "Pecho Mayor y Tríceps"),
        ("Press inclinado", "2 × 10", 90, "inclinado.mp4", "Pecho Superior"),
        ("Flexiones lentas", "2 × al fallo", 60, "flexiones.mp4", "Pecho y Core"),
        ("Press militar", "2 × 8", 90, "militar.mp4", "Hombros (Deltoide frontal)"),
        ("Fondos entre bancas", "2 × 12", 60, "fondos.mp4", "Tríceps")
    ],
    "Martes": [
        ("Remo con barra", "3 × 8–10", 90, "remo_barra.mp4", "Dorsales y Espalda Media"),
        ("Peso muerto rumano", "2 × 6–8", 120, "rumano.mp4", "Isquiotibiales y Glúteos"),
        ("Remo con mancuernas", "2 × 10", 90, "remo_man.mp4", "Dorsales (Unilateral)"),
        ("Curl bíceps barra", "2 × 10", 60, "curl_barra.mp4", "Bíceps"),
        ("Curl martillo", "2 × 12", 60, "martillo.mp4", "Bíceps y Braquial")
    ],
    "Miércoles": [
        ("Sentadilla con barra", "3 × 8", 120, "sentadilla.mp4", "Cuádriceps y Glúteos"),
        ("Sentadilla búlgara", "2 × 12", 90, "bulgara.mp4", "Cuádriceps y Estabilidad"),
        ("Zancadas", "2 × 10 por pierna", 90, "zancadas.mp4", "Glúteos y Piernas"),
        ("Elevación de talón", "2 × 15", 60, "talon.mp4", "Pantorrillas (Gastrocnemio)"),
        ("Plancha", "2 × 45–60 s", 45, "plancha.mp4", "Core (Abdominales profundos)"),
        ("Elevaciones de piernas", "2 × 12", 45, "elev_piernas.mp4", "Abdominales Inferiores")
    ],
    "Jueves": [
        ("Elevaciones laterales", "3 × 12", 45, "laterales.mp4", "Hombro Lateral (Ancho)"),
        ("Pájaros", "2 × 12", 60, "pajaros.mp4", "Hombro Posterior"),
        ("Fondos con banca", "2 × 12", 60, "fondos_banca.mp4", "Tríceps"),
        ("Curl concentrado", "1 × 12", 60, "concentrado.mp4", "Pico del Bíceps"),
        ("Plancha lateral", "2 × 30 s", 45, "plancha_lat.mp4", "Oblicuos"),
        ("Crunch lento", "2 × 15", 45, "crunch.mp4", "Abdominales Superiores")
    ],
    "Viernes": [
        ("Remo barra (ligero)", "2 × 12", 90, "remo_ligero.mp4", "Espalda (Técnica)"),
        ("Pullover mancuerna", "2 × 12", 90, "pullover.mp4", "Dorsal y Pecho"),
        ("Curl bíceps mancuernas", "2 × 12", 60, "biceps_man.mp4", "Bíceps"),
        ("Hollow hold", "2 × 30 s", 45, "hollow.mp4", "Core Estático"),
        ("Crunch lento", "2 × 15", 45, "crunch.mp4", "Abdomen")
    ]
}

if dia_actual_es in rutinas:
    for ej, reps, sec, archivo_nom, musculo in rutinas[dia_actual_es]:
        hecho = ej in st.session_state.completados
        with st.expander(f"🏋️ {ej}"):
            # Información del ejercicio
            st.info(f"🎯 **Músculo:** {musculo}")
            st.markdown(f"### **Objetivo: {reps}**")
            
            archivo_real = buscar_video(archivo_nom)
            if archivo_real:
                st.video(archivo_real)
            else:
                st.warning(f"Sube {archivo_nom} para ver el video.")

            if st.checkbox(f"Serie terminada", key=ej, value=hecho, disabled=hecho):
                if not hecho:
                    descanso(ej, sec)
else:
    st.success("¡Día de descanso! 🛌 Tiempo de reparar el tejido muscular.")

st.divider()
if st.button("🔄 Resetear día"):
    st.session_state.completados = []
    st.rerun()
