from database.database import Database
import config

db = Database() 

def guardar_venta(cliente, productos, fecha):
    print("\n=== DEBUG: ENTRANDO A GUARDAR VENTA ===")
    print(f"Cliente recibido: {cliente}")
    print(f"Productos recibidos en el MODELO: {productos}")
    print(f"Usuario activo guardando: {config.USUARIO_CONECTADO_ID}") # Debug para validar que llegue el ID real
    print("=======================================\n")

    query_cliente = """
    SELECT id_cliente FROM clientes WHERE nombre = %s
    """
    resultado = db.query_one(query_cliente, (cliente,))

    if resultado is None:
        raise Exception(f"El cliente '{cliente}' no existe en la base de datos")

    id_cliente = resultado["id_cliente"]

    total = sum(p["precio"] * p["cantidad"] for p in productos)

    query_venta = """
    INSERT INTO ventas(id_cliente, id_usuario, total, metodo_pago, fecha_venta)
    VALUES (%s, %s, %s, %s, NOW())
    """

    db.execute(query_venta, (id_cliente, config.USUARIO_CONECTADO_ID, total, "Efectivo"))

    resultado_id = db.query_one("SELECT MAX(id_venta) AS id_venta FROM ventas")
    id_venta = resultado_id["id_venta"]
    
    if id_venta is None:
        id_venta = 1

    print(f"-> ID REAL ASIGNADO PARA DETALLES: {id_venta}")

    for producto in productos: 
        query_producto = """
        SELECT id_producto, stock
        FROM productos
        WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(%s))
        """
        producto_db = db.query_one(query_producto, (producto["nombre"],))

        if producto_db is None:
            print(f"❌ ERROR CRÍTICO: El producto '{producto['nombre']}' NO SE ENCONTRÓ en la tabla productos. Saltando...")
            continue

        id_producto = producto_db["id_producto"]
        stock_actual = producto_db["stock"]

        if stock_actual < producto["cantidad"]:
            raise Exception(f"No hay suficiente inventario de {producto['nombre']}")

        query_update = """
        UPDATE productos SET stock = stock - %s WHERE id_producto = %s
        """
        db.execute(query_update, (producto["cantidad"], id_producto))

        subtotal = producto["precio"] * producto["cantidad"]

        query_detalle = """
        INSERT INTO detalle_ventas(id_venta, id_producto, cantidad, precio_unitario, subtotal)
        VALUES (%s, %s, %s, %s, %s)
        """
        db.execute(query_detalle, (id_venta, id_producto, producto["cantidad"], producto["precio"], subtotal))
        print(f"✅ DETALLE GUARDADO: {producto['nombre']} agregado a la venta #{id_venta}")


def obtener_ventas():
    query = """
    SELECT
        v.id_venta,
        c.nombre AS cliente_nombre,
        v.total,
        v.fecha_venta
    FROM ventas v
    INNER JOIN clientes c ON v.id_cliente = c.id_cliente
    WHERE v.id_usuario = %s  # 🌟 ¡FILTRO MULTIUSUARIO MÁGICO!
    ORDER BY v.id_venta DESC
    """

    ventas_db = db.query(query, (config.USUARIO_CONECTADO_ID,))
    resultado = []

    for venta in ventas_db:
        # --- MODIFICADO: Agregamos p.unidad en el SELECT ---
        detalle_query = """
        SELECT
            p.nombre,
            p.unidad,
            dv.precio_unitario,
            dv.cantidad
        FROM detalle_ventas dv
        INNER JOIN productos p ON dv.id_producto = p.id_producto
        WHERE dv.id_venta = %s
        """
        detalles = db.query(detalle_query, (venta["id_venta"],))
        productos = []

        for d in detalles:
            # --- MODIFICADO: Mapeamos la unidad para que Flet la lea ---
            productos.append({
                "nombre": d["nombre"],
                "precio": float(d["precio_unitario"]),
                "cantidad": d["cantidad"],
                "unidad": d["unidad"] if d["unidad"] else "" # Mandamos la unidad del producto vendido
            })

        resultado.append({
            "id_venta": venta["id_venta"],
            "cliente": venta["cliente_nombre"],
            "total": float(venta["total"]),
            "fecha_venta": venta["fecha_venta"],
            "productos": productos
        })

    return resultado