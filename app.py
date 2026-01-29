import streamlit as st
from datetime import date
import time
import os

# Configuración de la página
st.set_page_config(page_title="Toji Mode", page_icon="💪", layout="centered")

# --- LÓGICA DINÁMICA DE FECHA Y RACHA ---
# Fecha de inicio: 28 de enero de 2026
fecha_inicio = date(2026, 1, 28) 
hoy = date.today()

# Cálculo de racha: hoy es el día 1
racha_actual = (hoy - fecha_inicio).days + 1

# Traductor de días del sistema a español
dias_traduccion = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
nombre_dia_ingles = hoy.strftime("%A")
dia_actual = dias_traduccion.get(nombre_dia_ingles, "Lunes")

# --- INTERFAZ PRINCIPAL ---
st.title("🔥 Toji Mode: On")
st.metric(label="Racha de Entrenamiento", value=f"{racha_actual} Días")
st.subheader(f"Hoy es {dia_actual} ({hoy.strftime('%d/%m/%Y')})")

# Memoria de la sesión
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

# --- RUTINA Y ARCHIVOS MP4 ---
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

# Detector de archivos para ayuda visual
archivos_reales = os.listdir('.')

if dia_actual in rutinas:
    for ej, sec, archivo in rutinas[dia_actual]:
        ya_hecho = ej in st.session_state.completados
        
        with st.expander(f"🏋️ {ej}"):
            # Lógica de video local
            if os.path.exists(archivo):
                st.video(archivo)
            else:
                st.error(f"❌ No se encuentra: {archivo}")
                st.write(f"📂 Archivos en GitHub: {[f for f in archivos_reales if f.endswith('.mp4')]}")

            if st.checkbox(f"Marcar serie completa", key=ej, value=ya_hecho, disabled=ya_hecho):
                if not ya_hecho:
                    ejecutar_descanso(ej, sec)
else:
    st.success("¡Día de descanso! 🛌 Aprovecha para recuperar.")

st.divider()
if st.button("🔄 Resetear progreso de hoy"):
    st.session_state.completados = []
    st.rerun()
