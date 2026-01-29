import streamlit as st
from datetime import date
import time
import os

st.set_page_config(page_title="Toji Mode", page_icon="💪")

# --- LÓGICA DE RACHA ---
inicio = date(2026, 1, 28)
hoy = date.today()
racha = (hoy - inicio).days + 1

st.title("🔥 Toji Mode: On")
st.metric(label="Racha de Entrenamiento", value=f"{racha} Días")

if "completados" not in st.session_state:
    st.session_state.completados = []

def ejecutar_descanso(nombre, segundos):
    placeholder = st.empty()
    for t in range(segundos, -1, -1):
        placeholder.subheader(f"⏳ Descanso: {t}s")
        time.sleep(1)
    placeholder.success(f"¡Serie de {nombre} terminada!")
    st.balloons()
    if nombre not in st.session_state.completados:
        st.session_state.completados.append(nombre)
        st.rerun()

# --- RUTINA ACTUALIZADA ---
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
        ("Curl bíceps barra (2x10)", 60, "curl_barra.mp4"),
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

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
dia_actual = dias[hoy.weekday()]

st.subheader(f"Hoy es {dia_actual}")

if dia_actual in rutinas:
    for ej, sec, archivo in rutinas[dia_actual]:
        ya_hecho = ej in st.session_state.completados
        with st.expander(f"🏋️ {ej}"):
            if os.path.exists(archivo):
                st.video(archivo)
            else:
                st.info(f"Sube '{archivo}' para ver la técnica.")
            
            if st.checkbox(f"Marcar serie", key=ej, value=ya_hecho, disabled=ya_hecho):
                if not ya_hecho:
                    ejecutar_descanso(ej, sec)
else:
    st.success("¡Descanso! 🛌 Recupera para la próxima semana.")

if st.button("🔄 Resetear día"):
    st.session_state.completados = []

    st.rerun()

# Busca esta parte en tu código y añade la línea del print:
with st.expander(f"🏋️ {ej}"):
    if os.path.exists(archivo):
        st.video(archivo)
    else:
        # Esto te dirá exactamente qué nombre está buscando la app
        st.error(f"Error: Buscando el archivo exacto: '{archivo}'")
        st.write(f"Archivos que SI detecto en la carpeta: {os.listdir('.')}")
