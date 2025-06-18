
from salario import calcular_basico_y_complementos
from bonos import calcular_unidades_bono_reglamentaria, calcular_monto_bonos
from descuentos import calcular_descuentos_legales, calcular_descuentos_gremiales

EXCLUIDOS_BONIFICACION = {"404", "405", "411", "420", "422", "423"}

def calcular_simulacion(cargos, cantidades, puntajes_dict, vi, antiguedad, gremios):
    datos = calcular_basico_y_complementos(cargos, cantidades, puntajes_dict, vi, antiguedad)
    bonificacion_total = 0
    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        codigo = cargo.split(" - ")[0].strip()
        descripcion = cargo.lower()
        puntaje = puntajes_dict.get(cargo, 0)
        if "hora" in descripcion and (
            (codigo.startswith("3") or codigo.startswith("4")) and
            codigo not in EXCLUIDOS_BONIFICACION
        ):
            bonificacion_total += (puntaje * cantidades[i] * vi) * 0.2775

    unidades = calcular_unidades_bono_reglamentaria(datos["simples"], datos["completo"], datos["total_horas"])
    bonos = calcular_monto_bonos(unidades)
    legales = calcular_descuentos_legales(datos["remunerativo"])
    gremial = calcular_descuentos_gremiales(datos["remunerativo"], bonos, gremios)
    total_descuentos = legales["total_legales"] + gremial
    neto = datos["remunerativo"] - total_descuentos + bonos + bonificacion_total

    return {
        "Básico": datos["basico"],
        "Función Docente": datos["funcion_docente"],
        "Antigüedad": datos["antiguedad"],
        "Transformación": datos["transformacion"],
        "Zona": datos["zona"],
        "Adicional Jerárquico": datos["adicional_jerarquico"],
        "Remunerativo": datos["remunerativo"],
        "Bonificación Docente": bonificacion_total,
        "Bonos": bonos,
        "Descuentos Legales": legales["total_legales"],
        "Descuento Gremial": gremial,
        "Total Descuentos": total_descuentos,
        "NETO": neto,
        "Horas Totales": datos["total_horas"],
        "Unidades Bono": unidades
    }
