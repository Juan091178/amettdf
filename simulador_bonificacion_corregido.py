
import pandas as pd

VALOR_INDICE = 85.056195

# Diccionario de puntajes de ejemplo (reemplazar con carga real)
puntajes_dict = {
    "312 - HORA CÁTEDRA MODALIDAD ESPECIAL": 65.13,
    "421 - HORA CÁTEDRA NIVEL JÓVENES Y ADULTOS": 65.13,
    "852 - HORA CÁTEDRA SECUNDARIA": 65.13,
}

# Cargos de ejemplo
cargos = [
    "312 - HORA CÁTEDRA MODALIDAD ESPECIAL",
    "421 - HORA CÁTEDRA NIVEL JÓVENES Y ADULTOS",
    "852 - HORA CÁTEDRA SECUNDARIA"
]
cantidades = [1, 1, 1]

def calcular_antiguedad_factor(antiguedad):
    tabla = {
        range(0, 6): 0.40, range(6, 8): 0.50, range(8, 10): 0.60,
        range(10, 12): 0.70, range(12, 14): 0.80, range(14, 16): 0.90,
        range(16, 18): 1.00, range(18, 20): 1.10, range(20, 22): 1.20,
        range(22, 24): 1.30, range(24, 100): 1.35
    }
    for r in tabla:
        if antiguedad in r:
            return tabla[r]
    return 0

def calcular_total(cargos, cantidades, vi, puntajes_dict, antiguedad):
    total_puntaje = 0
    bonificacion_total = 0.0

    codigos_excluidos = {"404", "405", "411", "420", "422", "423"}

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        codigo = cargo.split(" - ")[0]
        descripcion = cargo.lower()
        puntaje = puntajes_dict.get(cargo, 0)
        total_puntaje += puntaje * cantidades[i]

        if "hora" in descripcion and (
            (codigo.startswith("3") or codigo.startswith("4")) and
            codigo not in codigos_excluidos
        ):
            bonificacion_total += (puntaje * cantidades[i] * vi) * 0.2795

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
    total_descuentos = jubilacion + obra_social + seguro

    neto = total_remun - total_descuentos + bonificacion_total

    return {
        "Básico": basico,
        "Función Docente": funcion_docente,
        "Antigüedad": antiguedad_valor,
        "Transformación": transformacion,
        "Zona": zona,
        "Remunerativo": total_remun,
        "Descuentos": total_descuentos,
        "Bonificación Docente": bonificacion_total,
        "NETO": neto
    }

# Ejecutar cálculo de ejemplo
resultado = calcular_total(cargos, cantidades, VALOR_INDICE, puntajes_dict, antiguedad=10)
for k, v in resultado.items():
    print(f"{k}: ${v:,.2f}")
