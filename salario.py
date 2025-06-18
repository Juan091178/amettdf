
from antiguedad import calcular_antiguedad_factor

JERARQUICOS = {"954","814","800","302","820","806","809","804","210","501","202","200",
    "826","208","803","400","402","502","837","204","827","206","107","811",
    "700","901","828","407","301","201","300","821","862","905","500","817",
    "207","813","203","401","601","511","822","818","105","906","408","805",
    "864","812","952","949","303","406","825","211","953","103","403","405",
    "819","513","205","838","512","824","815","807","802","902","808","816",
    "823","900","951","602","106","101","104","404","600","810","801","209",
    "102","950"}

EXCLUIDOS_BONIFICACION = {"404", "405", "411", "420", "422", "423"}

def calcular_basico_y_complementos(cargos, cantidades, puntajes_dict, vi, antiguedad):
    total_puntaje = 0
    basico_jerarquico = 0
    bonificacion_total = 0
    total_horas = 0
    simples = 0
    completo = False

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        codigo = cargo.split(" - ")[0].strip()
        puntaje = puntajes_dict.get(cargo, 0)
        total_puntaje += puntaje * cantidades[i]
        if codigo in JERARQUICOS:
            basico_jerarquico += puntaje * cantidades[i] * vi
        if "HORA" in cargo.upper():
            total_horas += cantidades[i]
        elif "COMPLETO" in cargo.upper():
            completo = True
        elif "SIMPLE" in cargo.upper():
            simples += 1
        descripcion = cargo.lower()
        if "hora" in descripcion and (
            (codigo.startswith("3") or codigo.startswith("4")) and
            codigo not in EXCLUIDOS_BONIFICACION
        ):
            bonificacion_total += (puntaje * cantidades[i] * vi) * 0.2775

    basico = total_puntaje * vi
    adicional_jerarquico = basico_jerarquico * 0.30
    funcion_docente = basico * 2.30
    antiguedad_valor = basico * calcular_antiguedad_factor(antiguedad)
    transformacion = basico * 1.23

    subtotal = basico + funcion_docente + antiguedad_valor + transformacion + adicional_jerarquico + bonificacion_total
    zona = subtotal
    remunerativo = subtotal + zona

    return {
        "basico": basico,
        "funcion_docente": funcion_docente,
        "antiguedad": antiguedad_valor,
        "transformacion": transformacion,
        "bonificacion_docente": bonificacion_total,
        "adicional_jerarquico": adicional_jerarquico,
        "subtotal": subtotal,
        "zona": zona,
        "remunerativo": remunerativo,
        "total_horas": total_horas,
        "simples": simples,
        "completo": completo
    }
