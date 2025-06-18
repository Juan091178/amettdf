
import streamlit as st
import pandas as pd
from simulador import calcular_simulacion

VALOR_INDICE_ABRIL = 85.056195
VALOR_INDICE_MAYO = 87.608881

@st.cache_data
def cargar_datos():
    df = pd.read_excel("Cargos_Abril2025.xlsx", sheet_name="Simulador Abril 2025")
    df["IDENTIFICADOR"] = df["COD."].astype(str).str.strip() + " - " + df["CARGO"].str.strip()
    return (
        dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 04/2025"])),
        dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 05/2025"])),
        df["IDENTIFICADOR"].dropna().tolist()
    )

puntajes_abril, puntajes_mayo, lista_cargos = cargar_datos()

st.title("📊 Simulador Salarial Docente – AMET TDF")

antiguedad = st.number_input("Antigüedad (años):", min_value=0, max_value=40, value=0)

st.markdown("### Selección de cargos/horas")
cargos_selec = []
cantidades = []

for i in range(3):
    col1, col2 = st.columns([3, 1])
    with col1:
        c = st.selectbox(f"Cargo #{i+1}", options=[""] + sorted(lista_cargos), key=f"cargo_{i}")
    with col2:
        q = st.number_input("Cantidad:", min_value=0, value=0, key=f"cantidad_{i}")
    cargos_selec.append(c)
    cantidades.append(q)

gremios_disponibles = ["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"]
gremio1 = st.selectbox("Gremio 1:", ["Ninguno"] + gremios_disponibles)
gremio2 = st.selectbox("Gremio 2:", ["Ninguno"] + gremios_disponibles)

descuentos = []
if gremio1 != "Ninguno":
    descuentos.append(gremio1)
if gremio2 != "Ninguno" and gremio2 != gremio1:
    descuentos.append(gremio2)

if st.button("Calcular Comparación Abril vs Mayo"):
    abril = calcular_simulacion(cargos_selec, cantidades, puntajes_abril, VALOR_INDICE_ABRIL, antiguedad, descuentos)
    mayo = calcular_simulacion(cargos_selec, cantidades, puntajes_mayo, VALOR_INDICE_MAYO, antiguedad, descuentos)

    df_resultado = pd.DataFrame({
        "Concepto": list(abril.keys()),
        "Abril ($)": list(abril.values()),
        "Mayo ($)": list(mayo.values()),
        "Diferencia ($)": [mayo[k] - abril[k] if isinstance(abril[k], (int, float)) else 0 for k in abril],
        "Variación (%)": [((mayo[k] - abril[k]) / abril[k] * 100) if isinstance(abril[k], (int, float)) and abril[k] != 0 else 0 for k in abril]
    })

    st.dataframe(df_resultado.style.format({
        "Abril ($)": "{:,.2f}",
        "Mayo ($)": "{:,.2f}",
        "Diferencia ($)": "{:,.2f}",
        "Variación (%)": "{:+.2f}%"
    }))

    diferencia_neta = mayo["NETO"] - abril["NETO"]
    st.markdown("### 🧾 Resultado final:")
    st.markdown(f"**Diferencia real (NETO Mayo - NETO Abril):** ${diferencia_neta:,.2f}")
