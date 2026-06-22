from database.database import Database

db = Database()

def obtener_productos(termino=""):
    if termino:
        query = """
        SELECT *
        FROM productos
        WHERE nombre LIKE %s OR categoria LIKE %s
        """
        return db.query(query, (f"%{termino}%", f"%{termino}%"))
    else:
        query = """
        SELECT *
        FROM productos
        """
        return db.query(query)


def agregar_producto(
    nombre,
    descripcion,
    precio,
    stock,
    categoria,
    id_proveedor,
    unidad
):
    query_buscar = """
    SELECT id_producto, stock
    FROM productos
    WHERE nombre = %s
    """

    producto = db.query_one(query_buscar, (nombre,))

    if producto:
        query_update = """
        UPDATE productos
        SET stock = stock + %s
        WHERE id_producto = %s
        """
        db.execute(
            query_update,
            (
                stock,
                producto["id_producto"]
            )
        )
    else:
        query_insert = """
        INSERT INTO productos(
            nombre,
            descripcion,
            precio,
            stock,
            categoria,
            id_proveedor,
            unidad
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        db.execute(
            query_insert,
            (
                nombre,
                descripcion,
                precio,
                stock,
                categoria,
                id_proveedor,
                unidad
            )
        ) 