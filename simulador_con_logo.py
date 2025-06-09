
import streamlit as st
import pandas as pd

# Cargar imágenes institucionales
from PIL import Image
logo_oficial = Image.open("Amet Logo 1 (1).png")
banner_amet = Image.open("WhatsApp Image 2025-06-09 at 3.32.54 PM.jpeg")

# Mostrar cabecera institucional
col1, col2 = st.columns([3, 1])
with col1:
    st.image(banner_amet, use_column_width=True)
    st.markdown("<h1 style='text-align: center; color: #002060;'>Simulador Salarial Docente 2025</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #002060;'>AMET Tierra del Fuego – Regional XXIV</h4>", unsafe_allow_html=True)
with col2:
    st.image(logo_oficial, width=120)

# --- CONTINUACIÓN DEL SIMULADOR ---
st.markdown("### Esta es solo la cabecera de prueba visual.")

