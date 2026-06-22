from model.producto_model import (
    obtener_productos,
    agregar_producto
)


def listar_productos(termino=""):
    productos = obtener_productos(termino)
    lista = []
    for p in productos:
        lista.append({
            "id": p["id_producto"],
            "nombre": p["nombre"],
            "descripcion": p["descripcion"],
            "precio": p["precio"],
            "cantidad": p["stock"],
            "categoria": p["categoria"],
            "id_proveedor": p["id_proveedor"],
            "unidad": p["unidad"]
        })
    return lista


def registrar_producto(
    nombre,
    descripcion,
    precio,
    cantidad,
    categoria,
    id_proveedor, 
    unidad,

):
    if (
        nombre == ""
        or precio == ""
        or cantidad == ""
    ):
        return False

    agregar_producto(
        nombre,
        descripcion,
        precio,
        cantidad,
        categoria,
        id_proveedor,
        unidad,
    ) 
    return True