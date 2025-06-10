
import streamlit as st
import pandas as pd
from PIL import Image

# Cargar imágenes
banner_amet = Image.open("banner_amet.jpeg")
logo_oficial = Image.open("logo_amet.png")

st.image(banner_amet, use_container_width=True)
st.markdown("<h1 style='text-align: center; color: #002060;'>Simulador Salarial Docente 2025</h1>", unsafe_allow_html=True)

VALOR_INDICE_ABRIL = 85.056195
VALOR_INDICE_MAYO = 87.608881

GREMIOS = {
    "AMET": 0.015, "SUTEF": 0.02, "SUETRA": 0.02,
    "ATE": 0.022, "UDAF": 0.013, "UDA": 0.015, "UPCN": 0.022
}

antiguedad_tabla = {
    range(0, 6): 0.40, range(6, 8): 0.50, range(8, 10): 0.60,
    range(10, 12): 0.70, range(12, 14): 0.80, range(14, 16): 0.90,
    range(16, 18): 1.00, range(18, 20): 1.10, range(20, 22): 1.20,
    range(22, 24): 1.30, range(24, 100): 1.35
}

def calcular_antiguedad_factor(antiguedad):
    for r in antiguedad_tabla:
        if antiguedad in r:
            return antiguedad_tabla[r]
    return 0

@st.cache_data
def cargar_datos():
    df = pd.read_excel("Cargos_Abril2025.xlsx", sheet_name="Simulador Abril 2025")
    df["IDENTIFICADOR"] = df["COD."].astype(int).astype(str) + " - " + df["CARGO"].str.strip()
    return df

df = cargar_datos()

puntajes_abril = dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 04/2025"]))
puntajes_mayo = dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 05/2025"]))
lista_cargos = df["IDENTIFICADOR"].dropna().tolist()

def calcular_total(cargos, cantidades, vi, puntajes_dict, descuentos, antiguedad):
    total_puntaje = 0
    total_horas = 0
    simples = 0
    completo = False

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        puntaje = puntajes_dict.get(cargo, 0)
        puntaje_total = puntaje * cantidades[i]
        total_puntaje += puntaje_total

        if "HORA" in cargo.upper():
            total_horas += cantidades[i]
        elif "COMPLETO" in cargo.upper():
            completo = True
        elif "SIMPLE" in cargo.upper():
            simples += cantidades[i]

    unidades_bono = 38 if completo else min(19 * min(simples, 2) + total_horas, 38)

    basico = total_puntaje * vi
    funcion_docente = basico * 2.30
    antiguedad_valor = basico * calcular_antiguedad_factor(antiguedad)
    transformacion = basico * 1.23
    subtotal = basico + funcion_docente + antiguedad_valor + transformacion
    zona = subtotal
    total_remun = subtotal + zona

    jubilacion = total_remun * 0.16
    obra_social = total_remun * 0.03
    seguro = 3000
    descuentos_legales = jubilacion + obra_social + seguro

    gremial = 0.0
    for g in descuentos:
        gremial += GREMIOS.get(g, 0.0) * (total_remun + (unidades_bono * (90000 / 38)))

    bonos = unidades_bono * (90000 / 38) + unidades_bono * (142600 / 38)

    total_descuentos = descuentos_legales + gremial
        
    
    # Calcular bonificación docente
    codigos_excluidos_bonificacion = {"404", "405", "411", "420", "422", "423"}
    bonificacion_total = 0.0
    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        identificador_codigo = cargo.split(" - ")[0].strip()
        descripcion = cargo.lower()
        if "hora" in descripcion and (
            (identificador_codigo.startswith("3") or identificador_codigo.startswith("4")) and
            identificador_codigo not in codigos_excluidos_bonificacion
        ):
            puntaje = puntajes_dict.get(cargo, 0)
            bonificacion_total += (puntaje * cantidades[i] * vi) * 0.2795

