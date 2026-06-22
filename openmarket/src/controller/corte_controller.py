from model.corte_model import (
    obtener_corte,
    total_corte_hoy,
    obtener_actividad_reciente,
    obtener_corte_filtrado
)


def calcular_totales():
    pedidos = obtener_corte()

    total = sum(p["total"] for p in pedidos if p["total"] is not None)

    cantidad = len(pedidos)
    pendiente = 0 

    return total, cantidad, pendiente 


def obtener_actividad():
    return obtener_actividad_reciente()


def obtener_corte_dia():
    return total_corte_hoy()

def listar_cortes_por_periodo(tipo_filtro, numero_periodo):
    if tipo_filtro == "todas":
        return obtener_corte()
    return obtener_corte_filtrado(tipo_filtro, numero_periodo)