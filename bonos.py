
def calcular_unidades_bono_reglamentaria(simples, completo, horas):
    if completo:
        return 38
    if simples == 2:
        return 38
    if simples == 1 and horas >= 22:
        return 38
    if simples == 1 and horas < 22:
        return min(19 + horas, 38)
    if simples == 0:
        return min(horas, 38)
    return 0

def calcular_monto_bonos(unidades):
    bono1 = unidades * (90000 / 38)
    bono2 = unidades * (142600 / 38)
    return bono1 + bono2
