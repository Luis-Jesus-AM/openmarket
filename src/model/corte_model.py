from database.database import Database

db = Database()


def obtener_corte():

    query = """
    SELECT
        id_pedido,
        total,
        fecha_pedido
    FROM pedidos
    """

    return db.query(query)