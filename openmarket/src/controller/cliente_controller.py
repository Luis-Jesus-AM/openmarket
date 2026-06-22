from model.cliente_model import (
    obtener_clientes,
    agregar_cliente,
    existe_telefono
)

import re


def listar_clientes():

    clientes = obtener_clientes()

    lista = []

    for c in clientes:

        lista.append({
            "id": c["id_cliente"],
            "nombre": c["nombre"],
            "telefono": c["telefono"],
            "correo": c["correo"]
        })

    return lista


def registrar_cliente(nombre, telefono, correo):

    nombre = nombre.strip()
    telefono = telefono.strip()
    correo = correo.strip()

    if nombre == "" or telefono == "" or correo == "":
        return "campos_vacios"

    if not telefono.isdigit() or len(telefono) != 10:
        return "telefono_invalido"

    patron_correo = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(patron_correo, correo):
        return "correo_invalido"

    if existe_telefono(telefono):
        return "telefono_existente"

    agregar_cliente(nombre, telefono, correo)

    return "ok"