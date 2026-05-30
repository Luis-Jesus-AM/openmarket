from database.database import Database

db = Database()


def obtener_clientes():

    query = """
    SELECT id_cliente, nombre, telefono
    FROM clientes
    """

    return db.query(query)


def agregar_cliente(nombre, telefono):

    query = """
    INSERT INTO clientes(nombre, telefono)
    VALUES (%s, %s)
    """

    db.execute(query, (nombre, telefono))