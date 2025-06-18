import streamlit as st
from simulador_amet_jerarquico_REVISION_LIMPIO_FUNCIONAL import calcular_total

st.set_page_config(page_title="Simulador Salarial Docente 2025")

st.title("🧮 Simulador Salarial Docente 2025")
st.markdown("Carga tus datos para estimar tu sueldo neto.")

# Inputs simulados
cargos = ["852 - HORA CÁTEDRA NIVEL E.G.B. 3 Y POLIMODAL"]
cantidades = [16]
vi = 4875.18  # Valor índice
puntajes = {"852 - HORA CÁTEDRA NIVEL E.G.B. 3 Y POLIMODAL": 1.0}
descuentos = ["AMET"]
antiguedad = 13

if st.button("Calcular ejemplo"):
    resultado = calcular_total(cargos, cantidades, vi, puntajes, descuentos, antiguedad)
    st.write("📊 Resultado del cálculo:")
    st.json(resultado)