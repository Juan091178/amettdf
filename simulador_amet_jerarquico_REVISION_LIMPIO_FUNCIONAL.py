def calcular_antiguedad_factor(antiguedad):
    antiguedad_tabla = {
        range(1, 4): 0.40,
        range(4, 7): 0.45,
        range(7, 10): 0.55,
        range(10, 13): 0.70,
        range(13, 16): 0.85,
        range(16, 18): 0.95,
        range(18, 20): 1.00,
        range(20, 22): 1.10,
        range(22, 24): 1.20,
        range(24, 25): 1.30,
        range(25, 100): 1.35
    }
    for r in antiguedad_tabla:
        if antiguedad in r:
            return antiguedad_tabla[r]
    return 0

def calcular_total(cargos, cantidades, vi, puntajes_dict, descuentos, antiguedad):
    bonificacion_total = 0.0
    adicional_jerarquico_total = 0.0
    total_puntaje = 0
    total_horas = 0
    simples = 0
    completo = False
    transformacion = 0.0

    jerarquicos = {"954","814","800","302","820","806","809","804","210","501","202","200","826","208","803","400",
                   "402","502","837","204","827","206","107","811","700","901","828","407","301","201","300","821",
                   "862","905","500","817","207","813","203","401","601","511","822","818","105","906","408","805",
                   "864","812","952","949","303","406","825","211","953","103","403","405","819","513","205","838",
                   "512","824","815","807","802","902","808","816","823","900","951","602","106","101","104","404",
                   "600","810","801","209","102","950"}

    codigos_excluidos_bonificacion = {"404", "405", "411", "420", "422", "423"}

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        codigo = cargo.split(" - ")[0].strip()
        puntaje = puntajes_dict.get(cargo, 0)
        total_puntaje += puntaje * cantidades[i]
        if codigo in jerarquicos:
            adicional_jerarquico_total += puntaje * cantidades[i] * vi * 0.30
        if "HORA" in cargo.upper():
            total_horas += cantidades[i]
        elif "COMPLETO" in cargo.upper():
            completo = True
        elif "SIMPLE" in cargo.upper():
            simples += cantidades[i]
        descripcion = cargo.lower()
        if "hora" in descripcion and (
            (codigo.startswith("3") or codigo.startswith("4")) and
            codigo not in codigos_excluidos_bonificacion
        ):
            bonificacion_total += (puntaje * cantidades[i] * vi) * 0.2775

    basico = total_puntaje * vi
    funcion_docente = basico * 2.30
    antiguedad_valor = basico * calcular_antiguedad_factor(antiguedad)
    transformacion = basico * 1.23
    zona = basico + funcion_docente + antiguedad_valor + transformacion + adicional_jerarquico_total
    total_remun = zona * 2

    jubilacion = total_remun * 0.16
    obra_social = total_remun * 0.03
    seguro = 3000
    descuentos_legales = jubilacion + obra_social + seguro

    GREMIOS = {
        "AMET": 0.015, "SUTEF": 0.02, "SUETRA": 0.02,
        "ATE": 0.022, "UDAF": 0.013, "UDA": 0.015, "UPCN": 0.022
    }

    gremial = 0.0
    for g in descuentos:
        gremial += GREMIOS.get(g, 0.0) * total_remun

    bonos = min(38, (19 * min(simples, 2) + total_horas)) * (90000 / 38) + min(38, (19 * min(simples, 2) + total_horas)) * (142600 / 38)
    total_descuentos = descuentos_legales + gremial
    neto = total_remun - total_descuentos + bonos + bonificacion_total

    return {
        "Básico": basico,
        "Función Docente": funcion_docente,
        "Antigüedad": antiguedad_valor,
        "Transformación": transformacion,
        "Zona": zona,
        "Remunerativo": total_remun,
        "Bonificación Docente": bonificacion_total,
        "Adicional Jerárquico": adicional_jerarquico_total,
        "Bonos": bonos,
        "Descuentos Legales": descuentos_legales,
        "Descuento Gremial": gremial,
        "Total Descuentos": total_descuentos,
        "NETO": neto
    }