from database.database import Database

db = Database()

def obtener_usuarios():

    query = """
    SELECT *
    FROM usuarios
    """

    return db.query(query)


def obtener_usuario_por_correo(correo):
    query = """
    SELECT id_usuario, nombre, correo, contraseña, telefono
    FROM usuarios
    WHERE correo = %s
    """
    return db.query_one(query, (correo,))

def agregar_usuario(

    nombre,
    correo,
    contraseña,
    telefono
):

    query = """
    INSERT INTO usuarios(

        nombre,
        correo,
        contraseña,
        telefono

    )

    VALUES (%s, %s, %s, %s)
    """

    db.execute(

        query,

        (
            nombre,
            correo,
            contraseña,
            telefono
        )
    )