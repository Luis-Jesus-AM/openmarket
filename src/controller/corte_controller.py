from model.corte_model import obtener_corte
from datetime import datetime


def calcular_totales():

    pedidos = obtener_corte()

    total = sum(p[1] for p in pedidos)
    cantidad = len(pedidos)
    pendiente = total

    return total, cantidad, pendiente


def obtener_actividad():

    pedidos = obtener_corte()

    return pedidos[-5:]


def obtener_corte_dia():

    pedidos = obtener_corte()

    hoy = str(datetime.now().date())

    total_hoy = sum(
        p[1]
        for p in pedidos
        if str(p[2]) == hoy
    )

    return total_hoy