from database.database import Database

db = Database()


def obtener_proveedores():
    query = """
    SELECT
        id_proveedor,
        nombre,
        correo,
        telefono,
        producto_que_vende,
        direccion
    FROM proveedores
    """
    return db.query(query)


def actualizar_producto(id_proveedor, nuevo_producto):
    """
    Agrega un nuevo producto al proveedor.
    Si ya tiene productos, los concatena con coma.
    """
    try:
        # 1. Obtener el producto actual del proveedor
        query_obtener = """
        SELECT producto_que_vende 
        FROM proveedores 
        WHERE id_proveedor = %s
        """
        resultado = db.query(query_obtener, (id_proveedor,))
        
        if resultado and resultado[0]["producto_que_vende"]:
            # Si ya tiene productos, concatenar con coma
            producto_actualizado = resultado[0]["producto_que_vende"] + ", " + nuevo_producto
        else:
            # Si no tiene productos aún
            producto_actualizado = nuevo_producto
        
        # 2. Actualizar en la base de datos
        query_update = """
        UPDATE proveedores 
        SET producto_que_vende = %s 
        WHERE id_proveedor = %s
        """
        db.execute(query_update, (producto_actualizado, id_proveedor))
        return True
        
    except Exception as e:
        print(f"Error al actualizar producto del proveedor: {e}")
        return False


def agregar_proveedor(nombre, correo, telefono, producto_que_vende, direccion):
    """
    Inserta un nuevo proveedor en la base de datos.
    Retorna True si se guardó con éxito, False si hubo algún error.
    """
    try:
        # Validación extra: si los campos obligatorios vienen vacíos, detenemos el proceso
        # (Ajusta 'nombre' u otros campos según tus reglas de negocio)
        if not nombre or not nombre.strip():
            return False

        query = """
        INSERT INTO proveedores(
            nombre,
            correo,
            telefono,
            producto_que_vende,
            direccion
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        db.execute(
            query,
            (
                nombre.strip() if nombre else None,
                correo.strip() if correo else None,
                telefono.strip() if telefono else None,
                producto_que_vende.strip() if producto_que_vende else None,
                direccion.strip() if direccion else None
            )
        )
        return True # Retornamos True para que el controlador/vista sepa que todo salió bien
        
    except Exception as e:
        print(f"Error al insertar el proveedor: {e}")
        return False