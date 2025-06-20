
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
from simulador import calcular_simulacion
import base64

VALOR_INDICE_ABRIL = 85.056195
VALOR_INDICE_MAYO = 87.608881

banner_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAUA...AAABJRU5ErkJggg=="
logo_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAE...AAABJRU5ErkJggg=="

def cargar_imagen(path, fallback_b64=None):
    try:
        return Image.open(path)
    except:
        if fallback_b64:
            return Image.open(BytesIO(base64.b64decode(fallback_b64)))
        return None

@st.cache_data
def cargar_datos():
    df = pd.read_excel("Cargos_Abril2025.xlsx", sheet_name="Simulador Abril 2025")
    df["IDENTIFICADOR"] = df["COD."].astype(str).str.strip() + " - " + df["CARGO"].str.strip()
    return (
        dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 04/2025"])),
        dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 05/2025"])),
        df["IDENTIFICADOR"].dropna().tolist()
    )

# Mostrar banner
banner = cargar_imagen("banner_amet.jpeg", fallback_b64=banner_b64)
if banner:
    st.image(banner, use_column_width=True)
else:
    st.warning("⚠️ No se pudo mostrar el banner")

st.title("📊 Simulador Salarial Docente – AMET TDF")

puntajes_abril, puntajes_mayo, lista_cargos = cargar_datos()
antiguedad = st.number_input("Antigüedad (años):", min_value=0, max_value=40, value=0)

st.markdown("### Selección de cargos/horas")
cargos_selec = []
cantidades = []

for i in range(3):
    col1, col2 = st.columns([3, 1])
    with col1:
        c = st.selectbox("Cargo #{}".format(i+1), options=[""] + sorted(lista_cargos), key="cargo_{}".format(i))
    with col2:
        q = st.number_input("Cantidad:", min_value=0, value=0, key="cantidad_{}".format(i))
    cargos_selec.append(c)
    cantidades.append(q)

gremios_disponibles = ["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"]
gremio1 = st.selectbox("Gremio 1:", ["Ninguno"] + gremios_disponibles)
gremio2 = st.selectbox("Gremio 2:", ["Ninguno"] + gremios_disponibles)

descuentos = []
if gremio1 != "Ninguno": descuentos.append(gremio1)
if gremio2 != "Ninguno" and gremio2 != gremio1: descuentos.append(gremio2)

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

    def estilo_fila(row):
        if row["Concepto"] == "NETO":
            return ['background-color: #1f77b4; color: white; font-weight: bold; font-size: 1.1em;' for _ in row]
        else:
            return ['' for _ in row]

    st.dataframe(
        df_resultado.style
            .apply(estilo_fila, axis=1)
            .format(subset=["Abril ($)", "Mayo ($)", "Diferencia ($)"], formatter="{:,.2f}")
            .format({"Variación (%)": "{:+.2f}%"})
    )

    diferencia_neta = mayo["NETO"] - abril["NETO"]
    st.markdown("### 🧾 Resultado final:")
    st.markdown("**Diferencia real (NETO Mayo - NETO Abril):** ${:,.2f}".format(diferencia_neta))

    logo = cargar_imagen("logo_amet.png", fallback_b64=logo_b64)
    col1, col2 = st.columns([1, 3])
    if logo:
        with col1:
            st.image(logo, width=120)
    with col2:
        st.markdown("**AMET TDF: la voz que no negocia la dignidad docente.**")
        st.markdown("Una gestión que defiende, una organización que crece")
        st.markdown("**AMET TDF**")
