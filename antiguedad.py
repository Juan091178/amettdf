
def calcular_antiguedad_factor(antiguedad):
    tabla = {
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
    for r in tabla:
        if antiguedad in r:
            return tabla[r]
    return 0
