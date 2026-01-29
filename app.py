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
    "El dolor es temporal, el orgullo de Toji es para siempre. 🔥",
    "¿Eres el más fuerte porque entrenas, o entrenas porque eres el más fuerte? 💀",
    "Un paso más cerca de la perfección física. ¡Buen trabajo! 🦍",
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
# Ahora guardamos cuántas series llevas de cada ejercicio
if "series_completadas" not in st.session_state:
    st.session_state.series_completadas = {} # Formato: {"Nombre": int}

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

# --- RUTINA (Con número de series extraído) ---
# Formato: (Nombre, Reps, Descanso, Archivo, Músculo, Total Series)
rutinas = {
    "Lunes": [
        ("Press banca", "3 × 8–10", 90, "banca.mp4", "Pecho y Tríceps", 3),
        ("Press inclinado", "2 × 10", 90, "inclinado.mp4", "Pecho Superior", 2),
        ("Flexiones lentas", "2 × al fallo", 60, "flexiones.mp4", "Pecho y Core", 2),
        ("Press militar", "2 × 8", 90, "militar.mp4", "Hombros", 2),
        ("Fondos entre bancas", "2 × 12", 60, "fondos.mp4", "Tríceps", 2)
    ],
    "Miércoles": [
        ("Sentadilla con barra", "3 × 8", 120, "sentadilla.mp4", "Piernas", 3),
        ("Sentadilla búlgara", "2 × 12", 90, "bulgara.mp4", "Piernas", 2),
        ("Zancadas", "2 × 10", 90, "zancadas.mp4", "Glúteos", 2),
        ("Elevación de talón", "2 × 15", 60, "talon.mp4", "Pantorrillas", 2),
        ("Plancha", "2 × 60s", 45, "plancha.mp4", "Core", 2),
    ]
    # ... (Puedes añadir el resto aquí siguiendo el mismo formato de 6 elementos)
}

ejercicios_del_dia = rutinas.get(dia_actual_es, [])
total_ejercicios = len(ejercicios_del_dia)
completados_hoy = 0

if ejercicios_del_dia:
    for ej, reps, sec, archivo_nom, musculo, total_series in ejercicios_del_dia:
        # Obtener progreso actual del ejercicio
        progreso = st.session_state.series_completadas.get(ej, 0)
        
        with st.expander(f"{'✅' if progreso >= total_series else '🏋️'} {ej} ({progreso}/{total_series} series)"):
            st.info(f"🎯 **Músculo:** {musculo}")
            st.markdown(f"### **Objetivo: {reps}**")
            
            archivo_real = buscar_video(archivo_nom)
            if archivo_real: st.video(archivo_real)

            # Botón para marcar serie
            if progreso < total_series:
                if st.button(f"Completar Serie {progreso + 1}", key=f"btn_{ej}"):
                    st.session_state.series_completadas[ej] = progreso + 1
                    iniciar_descanso(sec)
                    st.rerun()
            else:
                st.success("¡Ejercicio terminado!")
                completados_hoy += 1

    # --- LÓGICA DE FIN DEL DÍA ---
    if total_ejercicios > 0 and completados_hoy == total_ejercicios:
        st.divider()
        st.balloons()
        st.success("### ¡ENTRENAMIENTO COMPLETADO!")
        # Frase aleatoria
        frase_dia = random.choice(frases)
        st.markdown(f"> **{frase_dia}**")

else:
    st.success("¡Día de descanso! 🛌 Tiempo de reparar el tejido muscular.")

st.divider()
if st.button("🔄 Resetear día"):
    st.session_state.series_completadas = {}
    st.rerun()
