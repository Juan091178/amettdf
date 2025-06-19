
from salario import calcular_basico_y_complementos
from bonos import calcular_unidades_bono_reglamentaria, calcular_monto_bonos
from descuentos import calcular_descuentos_legales, calcular_descuentos_gremiales

def calcular_simulacion(cargos, cantidades, puntajes_dict, vi, antiguedad, gremios):
    datos = calcular_basico_y_complementos(cargos, cantidades, puntajes_dict, vi, antiguedad)

    unidades = calcular_unidades_bono_reglamentaria(
        datos["simples"], datos["completo"], datos["total_horas"]
    )
    bonos = calcular_monto_bonos(unidades)

    descuentos_legales = calcular_descuentos_legales(datos["remunerativo"])
    descuentos_gremiales = calcular_descuentos_gremiales(datos["remunerativo"], bonos, gremios)

    total_descuentos = descuentos_legales["total_legales"] + descuentos_gremiales
    neto = datos["remunerativo"] - total_descuentos + bonos

    return {
        "BÁSICO": datos["basico"],
        "FUNCIÓN DOCENTE": datos["funcion_docente"],
        "ANTIGÜEDAD": datos["antiguedad"],
        "TRANSFORMACIÓN EDUCATIVA": datos["transformacion"],
        "BONIFICACIÓN DOCENTE": datos["bonificacion_docente"],
        "ADICIONAL JERÁRQUICO": datos["adicional_jerarquico"],
        "SUBTOTAL": datos["subtotal"],
        "ZONA": datos["zona"],
        "REMUNERATIVO": datos["remunerativo"],
        "DESCUENTO JUBILACIÓN (16%)": descuentos_legales["jubilacion"],
        "DESCUENTO OBRA SOCIAL (3%)": descuentos_legales["obra_social"],
        "SEGURO DE VIDA": descuentos_legales["seguro"],
        "DESCUENTO GREMIAL": descuentos_gremiales,
        "TOTAL DESCUENTOS": total_descuentos,
        "BONOS NO REMUNERATIVOS": bonos,
        "NETO": neto
    }
