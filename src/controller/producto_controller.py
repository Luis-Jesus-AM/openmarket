from model.producto_model import (

    obtener_productos,

    agregar_producto
)


def listar_productos():

    productos = obtener_productos()

    lista = []

    for p in productos:

        lista.append({

            "id": p[0],

            "nombre": p[1],

            "descripcion": p[2],

            "precio": p[3],

            "stock": p[4],

            "categoria": p[5],

            "id_proveedor": p[6]
        })

    return lista


def registrar_producto(

    nombre,
    descripcion,
    precio,
    stock,
    categoria,
    id_proveedor
):

    if (
        nombre == ""
        or precio == ""
        or stock == ""
    ):
        return False

    agregar_producto(

        nombre,
        descripcion,
        precio,
        stock,
        categoria,
        id_proveedor
    )

    return True