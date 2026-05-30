from database.database import Database

db = Database()


def crear_tabla_proveedores():

    query = """
    CREATE TABLE IF NOT EXISTS proveedores(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        empresa TEXT,
        contacto TEXT,
        telefono TEXT
    )
    """

    db.execute(query)


def obtener_proveedores():

    query = """
    SELECT * FROM proveedores
    """

    db.execute(query)

    return 


def agregar_proveedor(empresa, contacto, telefono):

    query = """
    INSERT INTO proveedores(

        empresa,
        contacto,
        telefono

    )

    VALUES (?, ?, ?)
    """

    db.execute(

        query,

        (
            empresa,
            contacto,
            telefono
        )
    )