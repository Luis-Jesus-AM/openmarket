from model.cliente_model import (
    obtener_clientes,
    agregar_cliente
)


def listar_clientes():

    clientes = obtener_clientes()

    lista = []

    for c in clientes:

        lista.append({
            "id": c[0],
            "nombre": c[1],
            "telefono": c[2]
        })

    return lista


def registrar_cliente(nombre, telefono):

    if nombre == "" or telefono == "":
        return False

    agregar_cliente(nombre, telefono)

    return True