from database.database import Database

db = Database()


def obtener_clientes():

    query = """
    SELECT id_cliente, nombre, telefono, correo
    FROM clientes
    """

    return db.query(query)


def existe_telefono(telefono):

    query = """
    SELECT id_cliente
    FROM clientes
    WHERE telefono = %s
    """

    resultado = db.query_one(query, (telefono,))

    return resultado is not None


def existe_cliente(nombre):

    query = """
    SELECT id_cliente
    FROM clientes
    WHERE nombre = %s
    """

    resultado = db.query_one(query, (nombre,))

    return resultado is not None


def agregar_cliente(nombre, telefono, correo):

    query = """
    INSERT INTO clientes(nombre, telefono, correo)
    VALUES (%s, %s, %s)
    """

    db.execute(query, (nombre, telefono, correo))