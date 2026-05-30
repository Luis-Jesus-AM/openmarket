from model.proveedor_model import (
    obtener_proveedores,
    agregar_proveedor
)


def listar_proveedores():

    proveedores = obtener_proveedores()

    lista = []

    for p in proveedores:

        lista.append({

            "id": p[0],

            "empresa": p[1],

            "contacto": p[2],

            "telefono": p[3]
        })

    return lista


def registrar_proveedor(

    empresa,
    contacto,
    telefono
):

    if (
        empresa == ""
        or contacto == ""
        or telefono == ""
    ):
        return False

    agregar_proveedor(

        empresa,
        contacto,
        telefono
    )

    return True