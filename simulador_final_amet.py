
import streamlit as st
import pandas as pd
from PIL import Image

# Configuración inicial
st.set_page_config(page_title="Simulador Salarial Docente 2025", layout="centered")

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

    codigos_excluidos_bonificacion = {"404", "405", "411", "420", "422", "423"}
    bonificacion_total = 0.0

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        puntaje = puntajes_dict.get(cargo, 0)
        puntaje_total = puntaje * cantidades[i]
        total_puntaje += puntaje_total

        codigo = cargo.split(" - ")[0].strip()
        descripcion = cargo.lower()
        if "hora" in descripcion and (
            (codigo.startswith("3") or codigo.startswith("4")) and
            codigo not in codigos_excluidos_bonificacion
        ):
            bonificacion_total += (puntaje * cantidades[i] * vi) * 0.2795

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
    neto = total_remun - total_descuentos + bonos + bonificacion_total

    return {
        "Básico": float(basico),
        "Función Docente": float(funcion_docente),
        "Antigüedad": float(antiguedad_valor),
        "Transformación": float(transformacion),
        "Zona": float(zona),
        "Remunerativo": float(total_remun),
        "Bonificación Docente": float(bonificacion_total),
        "Bonos": float(bonos),
        "Descuentos Legales": float(descuentos_legales),
        "Descuento Gremial": float(gremial),
        "Total Descuentos": float(total_descuentos),
        "NETO": float(neto)
    }, total_horas, simples, completo

# Interfaz
st.title("🧮 Simulador Salarial Docente 2025")

st.markdown("### Cargar hasta 3 cargos u horas")
antiguedad = st.number_input("Antigüedad (años):", min_value=0, max_value=40, value=0)
cargos_selec = []
cantidades = []

for i in range(3):
    col1, col2 = st.columns([3, 1])
    with col1:
        c = st.selectbox(f"Cargo #{i+1}", options=[""] + lista_cargos, key=f"selector_{i}")
    with col2:
        q = st.number_input("Cantidad:", min_value=0, value=0, key=f"cantidad_{i}")
    cargos_selec.append(c)
    cantidades.append(q)

gremio1 = st.selectbox("Gremio 1:", ["Ninguno"] + list(GREMIOS.keys()))
gremio2 = st.selectbox("Gremio 2:", ["Ninguno"] + list(GREMIOS.keys()))

descuentos = []
if gremio1 != "Ninguno": descuentos.append(gremio1)
if gremio2 != "Ninguno" and gremio2 != gremio1: descuentos.append(gremio2)

if st.button("Calcular Comparación"):
    abril, horas, simples, completo = calcular_total(cargos_selec, cantidades, VALOR_INDICE_ABRIL, puntajes_abril, descuentos, antiguedad)
    mayo, _, _, _ = calcular_total(cargos_selec, cantidades, VALOR_INDICE_MAYO, puntajes_mayo, descuentos, antiguedad)

    extra_total = 0  # Se puede agregar cálculo de horas extra si se desea
    neto_abril_real = abril["NETO"] + extra_total
    diferencia_real = mayo["NETO"] - neto_abril_real

    df_resultado = pd.DataFrame({
        "Concepto": list(abril.keys()),
        "Abril ($)": list(abril.values()),
        "Mayo ($)": list(mayo.values()),
        "Diferencia ($)": [mayo[k] - abril[k] for k in abril],
        "Variación (%)": [((mayo[k] - abril[k]) / abril[k] * 100) if abril[k] else 0 for k in abril]
    })

    st.dataframe(df_resultado.style.format(subset=["Abril ($)", "Mayo ($)", "Diferencia ($)"], formatter="{:,.2f}").format({"Variación (%)": "{:+.2f}%"}) )

    st.markdown("### 🧾 Resumen Final:")
    st.markdown(f"**NETO Abril:** ${abril['NETO']:,.2f}")
    st.markdown(f"**NETO Mayo:** ${mayo['NETO']:,.2f}")
    st.markdown(f"**Diferencia real (Mayo - Abril):** ${diferencia_real:,.2f}")

# Pie de página con imagen y texto
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; margin-top: 30px;'>
    <div style='flex: 1;'>
        <img src='https://raw.githubusercontent.com/amet-tierra-del-fuego/assets/main/logo_amet.png' width='140'>
    </div>
    <div style='flex: 2; text-align: right; font-size: 16px;'>
        <p><strong>AMET TDF: la voz que no negocia la dignidad docente.</strong></p>
        <p style='margin-top: -10px;'>Una gestión que defiende, una organización que crece</p>
        <p><strong>AMET TDF</strong></p>
    </div>
</div>
""", unsafe_allow_html=True)
