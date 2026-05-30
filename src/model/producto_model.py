from database.database import Database

db = Database()


def obtener_productos():

    query = """
    SELECT *
    FROM productos
    """

    db.execute(query)

    return db.query(query)


def agregar_producto(

    nombre,
    descripcion,
    precio,
    stock,
    categoria,
    id_proveedor
):

    query = """
    INSERT INTO productos(

        nombre,
        descripcion,
        precio,
        stock,
        categoria,
        id_proveedor

    )

    VALUES (%s, %s, %s, %s, %s, %s)
    """

    db.execute(

        query,

        (
            nombre,
            descripcion,
            precio,
            stock,
            categoria,
            id_proveedor
        )
    )