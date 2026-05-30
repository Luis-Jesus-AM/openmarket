from database.database import Database

db = Database()


def crear_tablas_ventas():

    query_ventas = """
    CREATE TABLE IF NOT EXISTS ventas(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        cliente TEXT,
        fecha TEXT
    )
    """

    db.execute(query_ventas)

    query_detalle = """
    CREATE TABLE IF NOT EXISTS detalle_ventas(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        venta_id INTEGER,

        producto TEXT,
        precio REAL,
        cantidad INTEGER
    )
    """

    db.execute(query_detalle)


def guardar_venta(cliente, productos, fecha):

    query = """
    INSERT INTO ventas(cliente, fecha)
    VALUES (?, ?)
    """

    db.execute(query, (cliente, fecha))

    venta_id = db.cursor.lastrowid

    for producto in productos:

        detalle = """
        INSERT INTO detalle_ventas(

            venta_id,
            producto,
            precio,
            cantidad

        )

        VALUES (?, ?, ?, ?)
        """

        db.execute(

            detalle,

            (
                venta_id,
                producto["nombre"],
                producto["precio"],
                producto["cantidad"]
            )
        )


def obtener_ventas():

    query = """
    SELECT * FROM ventas
    """

    db.execute(query)

    ventas = db.query(query)

    resultado = []

    for venta in ventas:

        detalle_query = """
        SELECT producto, precio, cantidad
        FROM detalle_ventas
        WHERE venta_id = ?
        """

        db.execute(detalle_query, (venta[0],))

        detalles = db.query(detalle_query, (venta[0],))

        productos = []

        for d in detalles:

            productos.append({

                "nombre": d[0],
                "precio": d[1],
                "cantidad": d[2]
            })

        resultado.append({

            "id": venta[0],
            "cliente": venta[1],
            "fecha": venta[2],
            "productos": productos
        })

    return resultado