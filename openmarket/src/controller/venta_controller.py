from model.venta_model import (
    guardar_venta,
    obtener_ventas 
)

def registrar_venta(cliente, productos, fecha):
    if not cliente or cliente.strip() == "":
        cliente = "Publico en general"


    if len(productos) == 0:
        return False

    guardar_venta(cliente, productos, fecha)
    return True

def listar_ventas():
    return obtener_ventas()