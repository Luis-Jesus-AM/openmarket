from model.venta_model import (
    guardar_venta,
    obtener_ventas
)


def registrar_venta(cliente, productos, fecha):

    if cliente == "":
        return False

    if len(productos) == 0:
        return False

    guardar_venta(cliente, productos, fecha)

    return True


def listar_ventas():

    return obtener_ventas()