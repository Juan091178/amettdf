
GREMIOS = {
    "AMET": 0.015, "SUTEF": 0.02, "SUETRA": 0.02,
    "ATE": 0.022, "UDAF": 0.013, "UDA": 0.015, "UPCN": 0.022
}

def calcular_descuentos_legales(remunerativo):
    jubilacion = remunerativo * 0.16
    obra_social = remunerativo * 0.03
    seguro = 3000.0
    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "total_legales": jubilacion + obra_social + seguro
    }

def calcular_descuentos_gremiales(remunerativo, bonos, gremios):
    total = 0.0
    for gremio in gremios:
        porcentaje = GREMIOS.get(gremio, 0.0)
        total += porcentaje * (remunerativo + bonos)
    return total
