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
    p.success("¡Siguiente serie!")
    st.balloons()

# --- RUTINA ACTUALIZADA (Lunes a Viernes) ---
# Formato: (Nombre, Reps, Descanso, Archivo, Músculo, Total Series)
rutinas = {
    "Lunes": [
        ("Press banca", "3 × 8–10", 90, "banca.mp4", "Pecho Mayor y Tríceps", 3),
        ("Press inclinado", "2 × 10", 90, "inclinado.mp4", "Pecho Superior", 2),
        ("Flexiones lentas", "2 × al fallo", 60, "flexiones.mp4", "Pecho y Core", 2),
        ("Press militar", "2 × 8", 90, "militar.mp4", "Hombros", 2),
        ("Fondos entre bancas", "2 × 12", 60, "fondos.mp4", "Tríceps", 2)
    ],
    "Martes": [
        ("Remo con barra", "3 × 8–10", 90, "remo_barra.mp4", "Dorsales", 3),
        ("Peso muerto rumano", "2 × 6–8", 120, "rumano.mp4", "Isquiotibiales", 2),
        ("Remo con mancuernas", "2 × 10", 90, "remo_man.mp4", "Dorsales", 2),
        ("Curl bíceps barra", "2 × 10", 60, "curl_barra.mp4", "Bíceps", 2),
        ("Curl martillo", "2 × 12", 60, "martillo.mp4", "Bíceps", 2)
    ],
    "Miércoles": [
        ("Sentadilla con barra", "3 × 8", 120, "sentadilla.mp4", "Cuádriceps", 3),
        ("Sentadilla búlgara", "2 × 12", 90, "bulgara.mp4", "Cuádriceps", 2),
        ("Zancadas", "2 × 10 por pierna", 90, "zancadas.mp4", "Glúteos", 2),
        ("Elevación de talón", "2 × 15", 60, "talon.mp4", "Pantorrillas", 2),
        ("Plancha", "2 × 45–60 s", 45, "plancha.mp4", "Core", 2),
        ("Elevaciones de piernas", "2 × 12", 45, "elev_piernas.mp4", "Abdominales", 2)
    ],
    "Jueves": [
        ("Elevaciones laterales", "3 × 12", 45, "laterales.mp4", "Hombro Lateral", 3),
        ("Pájaros", "2 × 12", 60, "pajaros.mp4", "Hombro Posterior", 2),
        ("Fondos con banca", "2 × 12", 60, "fondos_banca.mp4", "Tríceps", 2),
        ("Curl concentrado", "1 × 12", 60, "concentrado.mp4", "Bíceps", 1),
        ("Plancha lateral", "2 × 30 s", 45, "plancha_lat.mp4", "Oblicuos", 2),
        ("Crunch lento", "2 × 15", 45, "crunch.mp4", "Abdominales", 2)
    ],
    "Viernes": [
        ("Remo barra (ligero)", "2 × 12", 90, "remo_ligero.mp4", "Espalda", 2),
        ("Pullover mancuerna", "2 × 12", 90, "pullover.mp4", "Dorsal y Pecho", 2),
        ("Curl bíceps mancuernas", "2 × 12", 60, "biceps_man.mp4", "Bíceps", 2),
        ("Hollow hold", "2 × 30 s", 45, "hollow.mp4", "Core Estático", 2),
        ("Crunch lento", "2 × 15", 45, "crunch.mp4", "Abdomen", 2)
    ]
}

# Solo marcar como descanso Sábado y Domingo
es_descanso = dia_actual_es in ["Sábado", "Domingo"]

if not es_descanso:
    ejercicios_del_dia = rutinas.get(dia_actual_es, [])
    total_ejercicios = len(ejercicios_del_dia)
    ejercicios_completados_count = 0

    for ej, reps, sec, archivo_nom, musculo, total_series in ejercicios_del_dia:
        progreso = st.session_state.series_completadas.get(ej, 0)
        
        # Expander visual
        with st.expander(f"{'✅' if progreso >= total_series else '🏋️'} {ej} ({progreso}/{total_series})"):
            st.info(f"🎯 **Músculo:** {musculo}")
            st.write(f"**Objetivo:** {reps}")
            
            video = buscar_video(archivo_nom)
            if video: st.video(video)

            if progreso < total_series:
                if st.button(f"Completar Serie {progreso + 1}", key=f"btn_{ej}"):
                    st.session_state.series_completadas[ej] = progreso + 1
                    iniciar_descanso(sec)
                    st.rerun()
            else:
                st.success("¡Ejercicio terminado!")
                ejercicios_completados_count += 1

    # --- MENSAJE FINAL DEL DÍA ---
    if ejercicios_completados_count == total_ejercicios and total_ejercicios > 0:
        st.divider()
        st.balloons()
        st.success("## 🔥 ¡DÍA COMPLETADO!")
        st.info(random.choice(frases))

else:
    st.success("¡Día de descanso! 🛌 Tiempo de reparar el tejido muscular.")

st.divider()
if st.button("🔄 Resetear progreso de hoy"):
    st.session_state.series_completadas = {}
    st.rerun()
