
from salario import calcular_basico_y_complementos
from bonos import calcular_unidades_bono_reglamentaria, calcular_monto_bonos
from descuentos import calcular_descuentos_legales, calcular_descuentos_gremiales

def calcular_simulacion(cargos, cantidades, puntajes_dict, vi, antiguedad, gremios):
    datos = calcular_basico_y_complementos(cargos, cantidades, puntajes_dict, vi, antiguedad)
    unidades = calcular_unidades_bono_reglamentaria(datos["simples"], datos["completo"], datos["total_horas"])
    bonos = calcular_monto_bonos(unidades)
    legales = calcular_descuentos_legales(datos["remunerativo"])
    gremial = calcular_descuentos_gremiales(datos["remunerativo"], bonos, gremios)
    total_descuentos = legales["total_legales"] + gremial
    neto = datos["remunerativo"] - total_descuentos + bonos

    return {
        "Básico": datos["basico"],
        "Función Docente": datos["funcion_docente"],
        "Antigüedad": datos["antiguedad"],
        "Transformación": datos["transformacion"],
        "Bonificación Docente": datos["bonificacion_docente"],
        "Adicional Jerárquico": datos["adicional_jerarquico"],
        "Subtotal": datos["subtotal"],
        "Zona": datos["zona"],
        "Remunerativo": datos["remunerativo"],
        "Bonos": bonos,
        "Descuentos Legales": legales["total_legales"],
        "Descuento Gremial": gremial,
        "Total Descuentos": total_descuentos,
        "NETO": neto,
        "Horas Totales": datos["total_horas"],
        "Unidades Bono": unidades
    }
